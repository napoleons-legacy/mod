# Napoleon's Legacy

An alternate history mod for Victoria 2

Built off of HPM 0.4.5.2

## Installation

Either download the mod as a zip folder or copy over the `Napoleon's Legacy` folder and `.mod` file to your mod folder.

Or, download the mod via git in your terminal by doing:
```
git clone --depth=1 https://github.com/napoleons-legacy/mod.git
cd mod && python install.py
```

To download the mod before an update is released, change the clone command to:
```
git clone --depth=1 -b development https://github.com/napoleons-legacy/mod.git
```
or change the branch to `development` and download as a zip folder.

## Development

Before submitting a pull request, it is best to do:
```
python cleanup.py
```

This cleans up the file by using spaces over tabs, and UNIX line endings over Windows line endings, and more.

If adding localization, it is best to do:
```
pip install -r requirements.txt
python localization.py
```

If there are duplicates, resolve them.

## History

The events covered by the mod since the POD are documented [here](history.md).

The history of the mod is open to change as it is developed and the scenario is further developed.

## Credits

Thanks to the people at /gsg/ for creating a new frontend background, providing feedback on ideas, and just being /gsg/.
