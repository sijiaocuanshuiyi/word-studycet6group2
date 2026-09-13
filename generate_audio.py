# -*- coding: utf-8 -*-
"""
六级单词批量生成发音 mp3
用法: python generate_audio.py
"""
import os
import asyncio
import sys

AUDIO_DIR = "audio"
VOICE = "en-US-JennyNeural"
RETRIES = 3

# ===== 85个单词（从你的 words.html 提取）=====
WORDS = [
    "tanker","artifact","pending","blaze","absurd","cub","wholesome","premise",
    "preside","lofty","unify","porridge","empirical","trumpet","cripple","zigzag",
    "withhold","feast","yacht","navigate","rejoice","trivial","cylinder","hitherto",
    "oppress","comic","counteract","plaintiff","yawn","fortnight","carve","atrocity",
    "trillion","symmetry","plead","avail","olive","gleam","sponge","deplete","concurrent",
    "havoc","armor","flare","scrap","vegetation","menace","verse","blush","harass","infringe",
    "reconcile","rein","tribute","multitude","errand","terminate","tow","simultaneous","thorn",
    "spectator","tentative","innumerable","herald","jolly","referendum","warranty","prop","correlate",
    "regime","intercourse","outrage","squad","sneak","plaza",
    "derail","ardent","imminent","plausible","downgrade","petition","clamp","strait","appease","glossary"
    # 注意：上面是示例，你需要把完整的85个单词列表贴进来
]
# =============================================

os.makedirs(AUDIO_DIR, exist_ok=True)


async def generate(word, path):
    import edge_tts
    communicate = edge_tts.Communicate(word, VOICE)
    await communicate.save(path)


async def main():
    print("=" * 50)
    print(f"六级单词发音生成器")
    print(f"语音引擎: {VOICE}")
    print(f"目标目录: {os.path.abspath(AUDIO_DIR)}")
    print("=" * 50)

    try:
        import edge_tts
    except ImportError:
        print("ERROR: 请先运行 pip install edge-tts")
        sys.exit(1)

    total = len(WORDS)
    print(f"共 {total} 个单词，开始生成...\n")

    done = 0
    skipped = 0
    failed = []

    for i, word in enumerate(WORDS, 1):
        path = os.path.join(AUDIO_DIR, f"{word}.mp3")

        # 已存在且有效则跳过
        if os.path.exists(path) and os.path.getsize(path) > 100:
            skipped += 1
            print(f"[{i}/{total}] SKIP {word} (已存在)")
            continue

        success = False
        for attempt in range(1, RETRIES + 1):
            try:
                await generate(word, path)
                if os.path.exists(path) and os.path.getsize(path) > 100:
                    success = True
                    break
            except Exception as e:
                if attempt < RETRIES:
                    print(f"  retry {word} #{attempt}: {e}")
                await asyncio.sleep(0.5)

        if success:
            done += 1
            size = os.path.getsize(path)
            print(f"[{i}/{total}] OK   {word} ({size//1024}KB)")
        else:
            failed.append(word)
            print(f"[{i}/{total}] FAIL {word}")

    print("\n" + "=" * 50)
    print(f"完成! 新增: {done}, 跳过: {skipped}, 失败: {len(failed)}")
    if failed:
        print(f"失败单词: {failed}")
    print(f"输出目录: {os.path.abspath(AUDIO_DIR)}")
    print("=" * 50)


asyncio.run(main())