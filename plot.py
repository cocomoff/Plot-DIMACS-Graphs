import matplotlib.pyplot as plt
import dill
from os.path import exists
import numpy as np
import gzip
from tqdm import tqdm

def main(name="USA-road"):
    fn = f"{name}-d.NY.co.gz"
    city = fn.split(".")[-3]
    fn_dill = f"{name}-{city}-co.dill"

    latitude = None
    longitude = None

    if not exists(fn_dill):
        for (l, line) in tqdm(enumerate(gzip.open(fn, "r"))):
            line = line.strip().decode("utf-8")

            if l <= 20:
                print(l, line)

            # コメント飛ばす
            if line[0] == 'c':
                continue

            # 頂点数を読み込んだら初期化
            if line[0] == 'p':
                lsp = line.split(" ")
                n = int(lsp[4])
                latitude = np.zeros(n, dtype=np.float64)
                longitude = np.zeros(n, dtype=np.float64)

            # 頂点
            if line[0] == 'v':
                lsp = line.split(" ")
                vi = int(lsp[1]) - 1
                lat, lon = int(lsp[2]) / 1e6, int(lsp[3]) / 1e6
                latitude[vi] = lat
                longitude[vi] = lon

        # データの保存
        with open(fn_dill, "wb") as f:
            data = {
                "latitude": latitude, 
                "longitude": longitude,
                "source": fn
            }
            dill.dump(data, f)

    else:
        print(f"Data dill file exists: {fn_dill}")
        data = dill.load(open(fn_dill, "rb"))
        latitude = data["latitude"]
        longitude = data["longitude"]

    # 可視化
    f = plt.figure()
    a = f.gca()
    a.scatter(longitude, latitude, color="r", s=0.01)
    plt.savefig(f"{name}-{city}-nodes.png", bbox_inches="tight", facecolor="w", dpi=150)
    plt.close()



if __name__ == '__main__':
    main()