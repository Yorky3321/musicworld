import { Midi } from "https://cdn.skypack.dev/@tonejs/midi@2.0.27";
import { measure } from './vexflow_demo.js';                 // 從 vexflow_demo.js 導入每個小節的資訊

const noteMap = {                                            // 共用查表
        "c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4,
        "f": 5, "f#": 6, "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11
    };
let blob = null;                                             // 提前宣告同步變數

console.log("共有小節數：", measure.length);

document.getElementById("export-midi").addEventListener("click", () => {
    console.log("共有小節數：", measure.length);
    const midi = new Midi();                   // 構建midi檔
    const track = midi.addTrack();             // 構件音軌

    let currentTime = 0;                       // 初始化目前時間軸的位置（單位是秒）

    for (const noteGroup of measure) {
        for (const note of noteGroup) {
            const keys = note.getKeys();
            const duration = note.getDuration();

            if (duration.includes("r")) {                       // 休止符跳過
                currentTime += getDurationInSeconds(duration);
                continue;
            } else {
                const midiNote = convertKeyToMidiNumber(keys[0]);
                const dur = getDurationInSeconds(duration);

                if (midiNote) {                                    // 轉換流程
                    track.addNote({
                    midi: midiNote,
                    time: currentTime,
                    duration: dur
                    });
                }

                currentTime += dur;                            // 每處理一個音符，就把「目前時間」推進
            }
        }
    }

    const bytes = midi.toArray();                          // 把整個 MIDI 檔案轉換為 Uint8Array 格式（二進位資料）
    blob = new Blob([bytes], { type: "audio/midi" });            // 用 Blob 把資料包裝成一個檔案

    // 顯示兩個已設定的按鈕
    document.getElementById("download-midi").style.display = "inline-block";
    document.getElementById("download-wav").style.display = "inline-block";
});

document.getElementById("download-midi").addEventListener("click", () => {
  if (!blob) return alert("請先匯出 MIDI");

    const url = URL.createObjectURL(blob);                 // 產生相應的url
    const a = document.createElement("a");                 // 動態產生<a>元素並點及下載
    a.href = url;
    a.download = "My_Stave.mid";
    a.click();
    URL.revokeObjectURL(url);                              // 釋放臨時產生的url占用的記憶體
})

document.getElementById("download-wav").addEventListener("click", async () => {
    if (!blob) return alert("請先匯出 MIDI");

    const formData = new FormData();                              // 動態生成form表單傳送midi檔，並避免畫面重整
    formData.append("midi_file", blob, "export.mid");

    const response = await fetch("/transforming/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
        body: formData
    });

    if (!response.ok) {
        const errorText = await response.text();  // 用 text() 接住錯誤頁面
        console.error("轉檔錯誤頁面：", errorText);
        alert("轉檔失敗：" + response.status);
        return;
    }

    const wavBlob = await response.blob();  // ← 取得 blob 本體
    const url = URL.createObjectURL(wavBlob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "export.wav";
    a.click();
    URL.revokeObjectURL(url); // ✅ 記得釋放

});


function convertKeyToMidiNumber(keyString) {
    const [letter, octaveStr] = keyString.split("/");
    const octave = parseInt(octaveStr);

    if (!noteMap.hasOwnProperty(letter)) return null;

    return 12 * (octave + 1) + noteMap[letter];
}

function getDurationInSeconds(duration, bpm=120) {

    const quarterNoteTime = 60 / bpm;  // 可根據實際需要再調整換算，例如每拍 = 0.5 秒
    let time;

    // 提取基礎音符長度（如 "q", "16" 等）
    let base = duration.replace(/[dr]/g, "");

    // 移除 'd' 與 'r' 等修飾符，取得音符實際長度部分

    switch (base) {
            case "w": time =  4 * quarterNoteTime; break;       // 全音符
            case "h": time = 2 * quarterNoteTime; break;        // 二分音符
            case "q": time = 1 * quarterNoteTime; break;        // 四分音符
            case "8": time = 0.5 * quarterNoteTime; break;      // 8分音符
            case "16": time = 0.25 * quarterNoteTime; break;    // 16分音符
            default: time = quarterNoteTime; break;             // 預設會回傳四分音符的時間
        };

    if (duration.includes("d")) time *= 1.5;

    return time
}

function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}
