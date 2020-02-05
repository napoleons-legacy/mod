import collections
import csv
import os
import textwrap
from typing import Iterable, List, Tuple, TypeVar

import click

from util import MOD_DIRECTORY, process_directory

COLUMNS = ("Key", "English", "French", "German", "Polish", "Spanish", "Italian",
           "Swedish", "Czech", "Hungarian", "Dutch", "Portuguese", "Russian", "Finnish")

EXTENSIONS = ["csv"]

Row = List[str]
L = TypeVar("L", bound="Localization")
LG = TypeVar("LG", bound="LocalizationGroup")
Assoc = Tuple[str, Row]
AssocList = List[Assoc]


class LocalizationGroup:
    """A grouping of localization files in the game."""

    def __init__(self: LG) -> None:
        """Initialize file path to localization dictionary,
        duplicates to an empty default dictionary,
        and all_removed to an empty list.
        """
        self.localizations = {}
        self.duplicates = collections.defaultdict(list)
        self.all_removed = []

    def add(self: LG, local: L) -> None:
        """Add a localization entry to the group."""
        file_path = local.file_path
        self.localizations[file_path] = local

        for key, entry in local.entries.items():
            self.duplicates[key].append((file_path, entry))

        for key, entries in local.duplicates.items():
            for entry in entries:
                self.duplicates[key].append((file_path, entry))

    def filter(self: LG) -> None:
        """Deduplicates all registered localization files in the group."""
        self.drop_uniques()

        items = self.duplicates.items()
        total_duplicates = sum(map(lambda tup: len(tup[1]), items))
        click.secho(f"There are {total_duplicates} duplicates to be processed." +
                    " Press (Ctrl+C) to exit and save progress at any time.",
                    fg="bright_black")

        for key, assoc in items:
            removed = self.drop_duplicates(key, assoc)
            self.all_removed.append((key, removed))

    def export(self: LG) -> None:
        """Export all updated records to their respective files."""
        for local in self.localizations.values():
            local.export()

    def drop_uniques(self: LG) -> None:
        """Drop all entries that are designated as duplicate
        while only having one, unique occurrence."""
        self.duplicates = {k: v for (k, v) in self.duplicates.items()
                           if len(v) != 1}

    def echo_removed(self: LG) -> None:
        """Display all removed keys from the provided file path."""
        for removed in self.all_removed:
            key, assoc = removed
            for entry in assoc:
                file_path, _ = entry

                click.secho(f"Removed duplicate key `{key}` from {file_path}",
                            fg="red")

    def drop_duplicates(self: LG, key: str, assoc: AssocList) -> AssocList:
        """Drop all duplicated entries for the provided key and return the removed entries."""
        self.echo_entries(key, assoc)
        return self.prompt_deduplication(key, assoc)

    def echo_entries(self: LG, key: str, assoc: AssocList) -> None:
        """Display all found entries for the specified key."""
        click.secho(f"{len(assoc)} ", fg="cyan", bold=True, nl=False)
        click.secho(f"total entries found for key ", fg="white", nl=False)
        click.secho(key, fg="bright_blue", nl=False)
        click.secho(".\n", fg="white")

    def prompt_deduplication(self: LG, key: str, assoc: AssocList) -> AssocList:
        """Display a prompt to deduplicate specified entries."""
        for index, local in enumerate(assoc):
            file_path, entry = local
            entry_style = click.style(f"Entry {index + 1}", fg="bright_blue")
            file_style = click.style(f"({file_path})", fg="bright_yellow")

            entry_str = Localization.to_str(entry)
            wrapped = textwrap.wrap(entry_str,
                                    width=110,
                                    replace_whitespace=False)

            nt = "\n\t"
            local_style = click.style(nt + nt.join(wrapped), fg="white")

            click.echo(f"{entry_style} {file_style}{local_style}\n")

        self.prompt_files(assoc)

        choice_style = click.style("Which entry should be chosen?",
                                   fg="bright_red")

        choice_type = click.IntRange(1, index + 1)
        choice_suffix = click.style(": ", fg="bright_red")

        chosen_entry = click.prompt(choice_style,
                                    type=choice_type,
                                    prompt_suffix=choice_suffix)

        click.echo()

        assoc_removed = assoc[:chosen_entry - 1] + assoc[chosen_entry:]
        self.deduplicate(key, assoc[chosen_entry - 1], assoc_removed)
        return assoc_removed

    def prompt_files(self: LG, assoc: AssocList) -> None:
        """Display a prompt to open the provided files."""
        file_names = set(map(lambda tup: tup[0], assoc))

        file_names_repr = ", ".join(file_names)
        ending = "this file" if len(file_names) == 1 else "these files"

        first_style = click.style(f"Do you want to open {ending}?",
                                  fg="bright_green")
        if click.confirm(first_style):
            for file_name in file_names:
                click.launch(file_name)

    def deduplicate(self: LG, key: str, chosen: Assoc, assoc_removed: AssocList) -> None:
        """Drop duplicated entries and emplace the chosen entry
        over the original incase it is a duplicate.
        """
        file_path, entry = chosen
        self.localizations[file_path].entries[key] = entry

        for assoc in assoc_removed:
            file_path, entry = assoc
            local = self.localizations[file_path]
            local.drop_entry(key, entry)


# A global localization group.
localization_group = LocalizationGroup()


class Localization:
    """A model for any localization file in the game."""

    def __init__(self: L, file_path: str) -> None:
        """Initialize file path, entries, and duplicates
        with the file contents provided.
        """
        self.file_path = file_path
        self.entries = {}
        self.duplicates = collections.defaultdict(list)

        with open(file_path, "r", encoding="latin-1") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)  # drop the header

            keys = set()
            for row in reader:
                first = row[0]

                trimmed = row[:len(COLUMNS)]

                cleaned = [self.clean_junk(value) for value in trimmed]
                cleaned.extend([""] * (len(COLUMNS) - len(cleaned)))

                head, *tail = cleaned

                if first not in keys:
                    keys.add(first)
                    self.entries[head] = tail
                else:
                    self.duplicates[head].append(tail)

    def export(self: L) -> None:
        """Write a localization file over
        its csv file with updated records.
        """
        with open(self.file_path, "w", encoding="latin-1") as file:
            file.write(Localization.to_str(COLUMNS) + "\n")  # Header

            for key, entry in self.entries.items():
                output = Localization.to_str([key] + entry)
                file.write(output + "\n")

    def drop_entry(self: L, key: str, entry: Row) -> None:
        """Drop a key from the model if the provided entry matches."""
        self.duplicates.pop(key, None)

        if key in self.entries and entry == self.entries[key]:
            self.entries.pop(key)

    def clean_junk(self: L, value: str) -> str:
        chars = set(value.lower())
        chars.discard("x")
        chars.discard(",")
        return "" if len(chars) == 0 else value

    @classmethod
    def to_str(self: L, entry: Iterable[str]) -> str:
        """Output an iterable row as a semi-colon joined string with
        an extra semi-colon at the end.
        """
        return ";".join(entry) + ";"


def clean_localization(file_path: str) -> None:
    """Registers all localization models with the global group."""
    global localization_group
    localization = Localization(file_path)
    localization_group.add(localization)


def prompt_export() -> None:
    if len(localization_group.all_removed) == 0:
        return

    export_style = click.style("Do you want to save your changes?",
                               fg="bright_green")
    if click.confirm(export_style):
        localization_group.export()


if __name__ == "__main__":
    directory = os.path.join(MOD_DIRECTORY, "localisation")
    process_directory(directory, EXTENSIONS, clean_localization)

    try:
        localization_group.filter()
        localization_group.export()
        localization_group.echo_removed()
    except click.Abort:
        try:
            click.echo()
            localization_group.echo_removed()
            prompt_export()
        except click.Abort:
            pass