from pathlib import Path
import merge

SOURCES = [
    'https://raw.githubusercontent.com/nthack/IPTVM3U/HEAD/HKTW.m3u',
    'https://raw.githubusercontent.com/hujingguang/ChinaIPTV/main/HongKong.m3u8',
]

def main():
    output, seen = ['#EXTM3U'], set()
    for source in SOURCES:
        for metadata, stream in merge.read_source(source):
            key = (stream, tuple(metadata[1:]))
            if key not in seen:
                seen.add(key)
                output.extend(metadata + [stream])
    Path('hk_selected.m3u').write_text('\n'.join(output) + '\n', encoding='utf-8')
    print('Selected playlist entries:', len(seen))

if __name__ == '__main__':
    main()
