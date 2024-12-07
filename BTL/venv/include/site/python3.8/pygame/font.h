#ifndef PGFONT_INTERNAL_H
#define PGFONT_INTERNAL_H

#include <SDL_ttf.h>

/* Kiểm tra khởi tạo font */
#define FONT_INIT_CHECK() \\
    if (!(*(int*)PyFONT_C_API[2])) \\
        return RAISE(pgExc_SDLError, "Hệ thống font chưa được khởi tạo")

#include "include/pygame_font.h"

#define PYGAMEAPI_FONT_NUMSLOTS 3

/* Hàm khởi tạo font hỗ trợ tiếng Việt */
TTF_Font* InitVietnameseFont(const char* font_path, int font_size) {
    /* Khởi tạo hệ thống font */
    if (TTF_Init() == -1) {
        printf("Không thể khởi tạo TTF: %s\\n", TTF_GetError());
        return NULL;
    }

    /* Tải font từ file */
    TTF_Font* font = TTF_OpenFont(font_path, font_size);
    if (!font) {
        printf("Không thể tải font: %s\\n", TTF_GetError());
        return NULL;
    }

    /* Thiết lập hỗ trợ Unicode cho font */
    TTF_SetFontHinting(font, TTF_HINTING_LIGHT);
    TTF_SetFontKerning(font, 1); // Hỗ trợ kerning cho ký tự tiếng Việt

    return font;
}

/* Hàm giải phóng font */
void CleanupFont(TTF_Font* font) {
    if (font) {
        TTF_CloseFont(font);
    }
    TTF_Quit();
}

#endif /* ~PGFONT_INTERNAL_H */
