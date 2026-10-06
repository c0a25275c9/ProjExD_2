import os
import time  #表示時間設定のためのモジュール
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の大きさと速度を10段階で設定する
    戻り値：爆弾Surfaceのリスト、加速倍率のリスト
    """
    bb_imgs = []

    for r in range(1, 11):  #爆弾Surfaceのリスト
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  #黒い四隅を透明にする
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]  #加速度のリスト

    return bb_imgs, bb_accs

def gameover(screen: pg.Surface) -> None:  #Game Overの関数を追加
    black_scr = pg.Surface((WIDTH, HEIGHT))  #演習1：黒の背景を設定
    black_scr.fill((0, 0, 0))
    black_scr.set_alpha(200) #透明度設定

    font = pg.font.Font(None, 80)  #演習1：白字でGame Over
    text_scr = font.render("Game Over", True, (255, 255, 255))

    kk_img = pg.image.load("fig/8.png")  #こうかとん画像を呼び出す


    black_scr.blit(text_scr, [(WIDTH - text_scr.get_width()) // 2, (HEIGHT - text_scr.get_height()) // 2])  #演習1：Game OverのSurfaceを背景にblitする
    black_scr.blit(kk_img, [WIDTH // 4 - kk_img.get_width() // 2, HEIGHT // 2 - kk_img.get_height() // 2])  #演習1：左のこうかとん表示
    black_scr.blit(kk_img, [WIDTH * 3 // 4 - kk_img.get_width() // 2, HEIGHT // 2 - kk_img.get_height() // 2])  #演習1：右のこうかとん表示
    screen.blit(black_scr, [0, 0])  #演習1：黒背景のSurfaceをscreen Surfaceにblitする
    pg.display.update()
    time.sleep(5)  #5秒間表示させる

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル(横方向判定結果、縦方向判定結果)
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #練習2：赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  #練習2：黒い四隅を消す
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  #横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT) #縦座標用の乱数
    vx, vy = +5, +5  #練習2：爆弾の初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #kkとbbのrectが重なっていたら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  #横方向移動量
                sum_mv[1] += tpl[1]  #縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #どこかしらはみでてる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        level = min(tmr // 500, 9)  #追加機能2：時間に応じて爆弾を拡大・加速させる
        bb_img = bb_imgs[level]
        avx = vx * bb_accs[level]  #横方向の速度
        avy = vy * bb_accs[level]  #縦方向の速度
        bb_rct.move_ip(avx, avy)  #爆弾を移動
        center = bb_rct.center
        bb_rct.size = bb_img.get_size()
        bb_rct.center = center
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #yoko == False
            vx *= -1
        if not tate:  #tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  #練習2:爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
