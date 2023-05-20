Process:
1. Adjust some paths
2. execute sd_extract and hd_extract
3. (optional) execute sd_upscale
4. execute sd_make_mod and hd_make_mod
5. execute compare and open html document

pip library needed:
- ffmpeg-python (and ffmpeg installed in system)
- pandas
- Pillow

todo:
- localized texture missing at the moment!!!
- create and apply mappinglist hd -> sd
- mapping for single sprite
- fix image glitch hd export
- sprite json has some dummy values