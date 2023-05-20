import os
import io
import zlib
from PIL import Image

directory_in = r"D:\Programme\Steam\steamapps\common\Heroes of Might & Magic III - HD Edition\data"
directory_out = r"R:\test"

def main():
    for filename in os.listdir(directory_in):
        if filename.lower().endswith(".pak") and "x3" in filename:
            full_name = os.path.join(directory_in, filename)
            extract_pak(full_name)

def extract_pak(file):
    #adapted from quickbms
    with open(file, 'rb') as f:
        f.read(4) # dummy
        info_offset = int.from_bytes(f.read(4), byteorder='little')
        f.seek(info_offset)
        files = int.from_bytes(f.read(4), byteorder='little')
        offset_name = f.tell()
        for i in range(files):
            f.seek(offset_name)
            name = f.read(8).split(b'\0', 1)[0].decode()
            f.read(12) # dummy
            offset = int.from_bytes(f.read(4), byteorder='little')
            dummy_size = int.from_bytes(f.read(4), byteorder='little')
            chunks = int.from_bytes(f.read(4), byteorder='little')
            zsize = int.from_bytes(f.read(4), byteorder='little')
            size = int.from_bytes(f.read(4), byteorder='little')
            chunk_zsize_arr = []
            for j in range(chunks):
                chunk_zsize = int.from_bytes(f.read(4), byteorder='little')
                chunk_zsize_arr.append(chunk_zsize)
            chunk_size_arr = []
            for j in range(chunks):
                chunk_size = int.from_bytes(f.read(4), byteorder='little')
                chunk_size_arr.append(chunk_size)
            offset_name = f.tell()

            f.seek(offset)
            image_config = f.read(dummy_size).decode()
            offset += dummy_size

            data = bytearray(b'')
            data_compressed = bytearray(b'')
            for j in range(chunks):
                f.seek(offset)
                if chunk_zsize_arr[j] == chunk_size_arr[j]:
                    data += bytearray(f.read(chunk_size))
                else:
                    data_compressed += bytearray(f.read(zsize))
                offset += chunk_zsize
            data_compressed = zlib.decompress(data_compressed)
            if len(data) < len(data_compressed): data = data_compressed
            
            extract_images(os.path.basename(file), name, image_config, data)

def extract_images(file, name, image_config, data):
    img = Image.open(io.BytesIO(data))
    for line in image_config.split('\r\n'):
        tmp = line.split(' ')
        if len(tmp) == 12:
            img_name = tmp[0]
            img_x = int(tmp[6])
            img_y = int(tmp[7])
            img_width = int(tmp[8])
            img_height = int(tmp[9])
            img_rotation = int(tmp[10])

            img_crop = img.crop((img_x, img_y, img_x+img_width, img_y+img_height))
            img_crop = img_crop.rotate(-90 * img_rotation, expand=True)

            img_crop.save(directory_out + "\\" + img_name + ".png")
    img.save(directory_out + "\\" + name + ".png")

if __name__ == "__main__":
    main()
