import os
from PIL import Image

# --- 設定項目 ---

# 1. 背景画像の設定
BASE_IMAGE_WIDTH = 5000
BASE_IMAGE_HEIGHT = 3750
BASE_IMAGE_COLOR = (89, 156, 170)

# 2. 中央に配置する画像の設定
TARGET_HEIGHT = 2500

# 3. フォルダの設定
INPUT_FOLDER = 'input_images'
OUTPUT_FOLDER = 'output_images'


def process_images():
    """
    指定されたフォルダ内の画像ファイルを処理し、背景画像と合成して保存する関数
    """
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"フォルダ '{INPUT_FOLDER}' を作成しました。このフォルダ内に処理したいPNGやJPEG画像を入れてください。")
        return

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"フォルダ '{OUTPUT_FOLDER}' を作成しました。処理後の画像がここに保存されます。")

    try:
        supported_extensions = ('.png', '.jpeg', '.jpg')
        image_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(supported_extensions)]

        if not image_files:
            print(f"エラー: '{INPUT_FOLDER}' フォルダ内に処理対象の画像ファイルが見つかりません。")
            return

        print(f"{len(image_files)}個の画像ファイルを処理します...")

        for filename in image_files:
            # --- 1. 背景画像を生成 ---
            base_image = Image.new('RGB', (BASE_IMAGE_WIDTH, BASE_IMAGE_HEIGHT), BASE_IMAGE_COLOR)

            # --- 2. 貼り付ける画像を読み込み ---
            image_path = os.path.join(INPUT_FOLDER, filename)
            overlay_image = Image.open(image_path).convert("RGBA")

            # --- 3. 画像をリサイズ (アスペクト比を維持) ---
            original_width, original_height = overlay_image.size
            aspect_ratio = original_width / original_height
            new_width = int(TARGET_HEIGHT * aspect_ratio)
            resized_image = overlay_image.resize((new_width, TARGET_HEIGHT), Image.Resampling.LANCZOS)

            # --- 4. 貼り付け位置を計算 (中央揃え) ---
            paste_x = (BASE_IMAGE_WIDTH - new_width) // 2
            paste_y = (BASE_IMAGE_HEIGHT - TARGET_HEIGHT) // 2
            paste_position = (paste_x, paste_y)

            # --- 5. 画像を合成 ---
            base_image.paste(resized_image, paste_position, resized_image)

            # --- 6. 画像を保存 ---
            # 元のファイル名から拡張子を取り除き、.pngとして保存する
            file_basename, _ = os.path.splitext(filename)
            output_filename = f"{file_basename}.png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            # JPEGを貼り付けた場合でも、背景との合成品質を保つためPNGで出力します
            base_image.save(output_path, 'PNG')

            print(f" ✓ '{filename}' を処理し、'{output_path}' として保存しました。")

        print("\n全ての処理が完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

process_images()


