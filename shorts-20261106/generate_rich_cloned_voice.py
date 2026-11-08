import os, sys, time
import soundfile as sf
from voxcpm import VoxCPM

REPO_DIR = "/Users/garfiwang/Documents/Antigravity-2026/克隆語音"
voice_name = "rich的聲音"
ref_wav = os.path.join(REPO_DIR, "voices", voice_name, "ref_voice.wav")
ref_txt = os.path.join(REPO_DIR, "voices", voice_name, "prompt.txt")

with open(ref_txt, "r", encoding="utf-8") as f:
    prompt_text = f.read().strip()

out_dir = "/Users/garfiwang/Library/CloudStorage/GoogleDrive-richnews168@gmail.com/我的雲端硬碟/【筆記】每週財經資訊/shorts-20261106/audio"
os.makedirs(out_dir, exist_ok=True)

# 簡體中文輸入消除多音字與分詞偏誤，數字轉為大寫中文確保發音精準
scenes = [
    {
        "id": "s1_rich",
        "text": "你看懂这周市场的矛盾信号了吗？十年期美债殖利率跳水破百分之四点八三，费半却暴跌百分之二十坠入熊市。到底是在恐慌什么？"
    },
    {
        "id": "s2_rich",
        "text": "答案是：自由现金流的严酷考验！亚马逊第三季自由现金流重挫四百二十三亿美元，谷歌资本支出飙破一兆。市场不再买单无底洞式的本益比，没有实质造血能力的假AI泡沫，正在被无情挤压。"
    },
    {
        "id": "s3_rich",
        "text": "但先别慌张！标普预估本益比已降到十八点八倍，辉达甚至来到超跌的二十九倍。回顾美股四十四年中期选举历史，选举日前进场，后一年平均大涨百分之十一。当市场为短期杂音焦虑，就是长线赢家逢低捡钻石的时刻。"
    },
    {
        "id": "s4_rich",
        "text": "记住顶尖投资视角的两大纪律：第一，不融资、手握百分之五国库券筑起护城河；第二，大胆布局具备定价权与高自由现金流的巨头。市场越震荡，核心资产越珍贵。追踪Rich，每周带你穿透市场迷雾！"
    }
]

device = "mps"
print(f"Loading VoxCPM2 on {device} for Rich voice clone...", flush=True)
t0 = time.time()
model = VoxCPM.from_pretrained(
    "openbmb/VoxCPM2",
    load_denoiser=False,
    device=device,
    optimize=False
)
print(f"Model loaded in {time.time()-t0:.1f}s", flush=True)

for i, item in enumerate(scenes, 1):
    lid = item["id"]
    txt = item["text"]
    out_file = os.path.join(out_dir, f"{lid}.wav")
    print(f"[{i}/{len(scenes)}] Generating {lid} ({len(txt)} chars)...", flush=True)
    t_start = time.time()
    wav = model.generate(
        text=txt,
        prompt_wav_path=ref_wav,
        prompt_text=prompt_text,
        reference_wav_path=ref_wav,
        cfg_value=2.0,
        inference_timesteps=10
    )
    elapsed = time.time() - t_start
    dur = len(wav) / model.tts_model.sample_rate
    print(f"Generated {lid} in {elapsed:.1f}s (dur: {dur:.2f}s, RTF: {elapsed/dur:.1f})", flush=True)
    sf.write(out_file, wav, model.tts_model.sample_rate)

print("ALL RICH CLONED VOICEOVERS GENERATED SUCCESSFULLY!", flush=True)
