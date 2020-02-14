# planet_thumbs

A tool for downloading Planet Labs imagery thumbnails, like the one below.

![](example_thumbnail.jpg)

<p align="center">
  <sup><i>Augustine Volcano on 10 February 2020. Imagery © 2020 Planet Labs.</i></sup>
</p>

## Quickstart

**NOTE:** This tool requires a valid Planet Labs API key. Set the environment
variable `PL_API_KEY` to your key's value prior to running the script. To sign
up for the Planet Labs Education and Research Program, go
[here](https://www.planet.com/markets/education-and-research/).

1. Prepare
   ```
   conda create -n planet_thumbs -c conda-forge planet
   conda activate planet_thumbs
   ```

2. Obtain
   ```
   git clone https://github.com/liamtoney/planet_thumbs.git
   cd planet_thumbs
   ```

3. Run
   ```
   python planet_thumbs.py <alaskan_volcano_name>
   ```

## Example

To grab the most recent thumbnails for Korovin Volcano, run
```
python planet_thumbs.py korovin
```
which produces the following thumbnails (when run on 14 February 2020).
```
korovin_2020-02-03T22_02_25_167781Z_PSScene3Band.png
korovin_2020-01-29T21_58_46_150495Z_PSScene3Band.png
korovin_2020-01-16T22_16_49_817145Z_PSScene3Band.png
korovin_2019-12-20T22_03_44_716131Z_PSScene3Band.png
korovin_2019-04-30T22_25_04_25561Z_PSOrthoTile.png
```
