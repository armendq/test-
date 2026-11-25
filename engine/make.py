import sys, subprocess, os
import cairocffi as cairo
from lib import W, H, FPS, N
from scenes import draw

OUT = os.path.dirname(os.path.abspath(__file__))


def frame(surf, ctx, i):
    ctx.save(); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.restore()
    draw(ctx, i / FPS, i)


def main():
    mode = sys.argv[1]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    if mode == 'still':
        from PIL import Image
        ts = [float(x) for x in sys.argv[2].split(',')]
        cols = int(sys.argv[3]) if len(sys.argv) > 3 else len(ts)
        tw_, th_ = 360, 640
        rows = (len(ts) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * tw_, rows * th_), 'black')
        for k, t in enumerate(ts):
            frame(surf, ctx, int(round(t * FPS)))
            im = Image.frombuffer('RGBA', (W, H), bytes(surf.get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
            sheet.paste(im.resize((tw_, th_), Image.LANCZOS), ((k % cols) * tw_, (k // cols) * th_))
        sheet.save(os.path.join(OUT, sys.argv[4] if len(sys.argv) > 4 else 'sheet.jpg'), quality=88)
    elif mode == 'render':
        a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        b = int(sys.argv[3]) if len(sys.argv) > 3 else N
        out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(OUT, 'video.mp4')
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS),
                              '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out],
                             stdin=subprocess.PIPE)
        for i in range(a, b):
            frame(surf, ctx, i)
            p.stdin.write(bytes(surf.get_data()))
        p.stdin.close(); p.wait()


main()
