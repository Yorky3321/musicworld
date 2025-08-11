import * as VexFlow from 'https://cdn.skypack.dev/vexflow@4.2.3';
import * as Tone from 'https://unpkg.com/tone';
const VF = VexFlow;

// 主容器
const container = document.getElementById("staff-container");
const canvas = document.getElementById("score");
const renderer = new VF.Renderer(canvas, VF.Renderer.Backends.CANVAS);     // 初始化畫布
const context = renderer.getContext();                                     // 選定畫布
const firstGap = 80;                              // 設定第一欄的五線譜要預留的空位
let staveY = 20;                                  // 初始五線譜高度
let Xpos = 30;                                    // 初始五線譜X軸
let measure = [];                                 // 宣告音符總集
let note;                                         // 宣告每小節的音符集
let count = 0;                                    // 計數器用來設定初始譜面
let noteInfoList = [];                            // 存放所有音符的區域和位置資訊
let selectedNoteInfo = null;                      // 儲存被選到的 note 資訊

// ✅ 畫譜邏輯包成一個函式
function canvasCreate(width) {
  Xpos = 30;
  staveY = 20;
  canvas.width = width;
  canvas.height = 2000;
}

//  設定音符
function NoteSet(position, index, key, keyhigh, duration) {
  console.log("NoteSet被呼叫了")
  const notes = measure[position];
  notes[index] = new VF.StaveNote({ keys: [key+"/"+keyhigh], duration: duration });
  canvasCreate(window.innerWidth * 0.9);
  StaveRecreate();
}


// 初始化五線譜
function StaveCreate() {

  // 建立音符
  note = [
    new VF.StaveNote({ keys: ["b/4"], duration: "qr" }),
    new VF.StaveNote({ keys: ["b/4"], duration: "qr" }),
    new VF.StaveNote({ keys: ["b/4"], duration: "qr" }),
    new VF.StaveNote({ keys: ["b/4"], duration: "qr" }),
  ];
  measure.push(note);

  const notes = measure[count];
  const voice = new VF.Voice({ time: { num_beats: 4, beat_value: 4 } });
  voice.addTickables(notes);

  const formatter = new VF.Formatter();
  const minGap = notes.length * 35;   // 每個音符的間隔值
  let staveWidth = formatter.preCalculateMinTotalWidth([voice]) + minGap;
  if ((Xpos + staveWidth) > (container.clientWidth - 60) ) {
    staveY += 100;
    Xpos = 30;
  }

  let stave;                // 提前宣告變數stave

  if ( Xpos === 30) {                           // 判斷是否為第一個
      staveWidth += firstGap;
      stave = new VF.Stave(Xpos, staveY, staveWidth);    // 建立五線譜
      stave.addClef("treble").addTimeSignature("4/4");
    } else {
      stave = new VF.Stave(Xpos, staveY, staveWidth);    // 建立五線譜
    }

  stave.setContext(context).draw();                      // 畫出五線譜
  formatter.joinVoices([voice]).format([voice], stave.getWidth() - 60);      // 格式化音符
  voice.draw(context, stave);                            // 畫上音符
  let InfoList = notes.map((note, index) => {
    const bb = note.getBoundingBox();
    const info = {
      index,
      note,
      noteIndex: measure.findIndex(group => group.includes(note)),
      x: bb ? bb.getX() : null,
      y: bb ? bb.getY() : null,
      width: bb ? bb.getW() : null,
      height: bb ? bb.getH() : null,
      // pitch: note.keys,
      // duration: note.duration
    };
    return info
  });
  noteInfoList.push(InfoList);

  Xpos += staveWidth;
  count ++;
}

// 畫面改變時全部重畫
function StaveRecreate() {
  noteInfoList = []
  for (let i = 0; i < measure.length; i ++) {
    const notes = measure[i];
    const voice = new VF.Voice({ time: { num_beats: 4, beat_value: 4 } });
    voice.addTickables(notes);

    const formatter = new VF.Formatter();
    const minGap = notes.length * 35;   // 每個音符的間隔值
    let staveWidth = formatter.preCalculateMinTotalWidth([voice]) + minGap;
    if ((Xpos + staveWidth) > (container.clientWidth - 60) ) {
      staveY += 100;
      Xpos = 30;
    }
    let stave;                // 提前宣告變數stave

    if ( Xpos === 30) {                           // 判斷是否為第一個
      staveWidth += firstGap;
      stave = new VF.Stave(Xpos, staveY, staveWidth);    // 建立五線譜
      stave.addClef("treble").addTimeSignature("4/4");
    } else {
      stave = new VF.Stave(Xpos, staveY, staveWidth);    // 建立五線譜
    }
    stave.setContext(context).draw();
    //畫上音符
    formatter.joinVoices([voice]).format([voice], stave.getWidth() - 60);
    voice.draw(context, stave);
    // 以下程式碼用來標記並記錄每個音符的位置
    let InfoList = notes.map((note, index) => {
      const bb = note.getBoundingBox();
      const info = {                                     // 紀錄位置(每個音符)
        index,
        note,
        noteIndex: measure.findIndex(group => group.includes(note)),
        x: bb ? bb.getX() : null,
        y: bb ? bb.getY() : null,
        width: bb ? bb.getW() : null,
        height: bb ? bb.getH() : null,
        // pitch: note.keys,
        // duration: note.duration
      };

      if (selectedNoteInfo && selectedNoteInfo.note === note) {         // 藍色框選該音符
        context.beginPath();
        context.rect(info.x, info.y, info.width, info.height);
        context.strokeStyle = "blue";
        context.lineWidth = 2;
        context.stroke();
      }
      return info
    });
    noteInfoList.push(InfoList);

    Xpos += staveWidth;
  }
}

// 初次載入
canvasCreate(window.innerWidth * 0.9);
StaveCreate();

// 視窗尺寸改變時，重繪 canvas
window.addEventListener('resize', () => {
  canvasCreate(window.innerWidth * 0.9);
  StaveRecreate();
});

document.addEventListener('DOMContentLoaded', () => {
  const btnAdd = document.querySelector('button[data-action="add"]');
  const btnSet = document.querySelector('button[data-action="Note-Set"]');

  if (btnAdd) {
    btnAdd.addEventListener('click', () => {
      StaveCreate();
    });
  } else {
    console.warn('找不到 <button data-action="add">');
  }

  canvas.addEventListener("click", function (event) {
    // console.log(selectedNoteInfo);
    const rect = canvas.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const clickY = event.clientY - rect.top;

    let found = false;
    for (const noteGroup of noteInfoList) {
      for (const note of noteGroup) {
        if (
          clickX >= note.x &&
          clickX <= note.x + note.width &&
          clickY >= note.y &&
          clickY <= note.y + note.height
        ) {
          selectedNoteInfo = note;
          // console.log("選取音符：", note);
          found = true;
          break;
        }
      }
      if (found) break;
    };
    canvasCreate(window.innerWidth * 0.9);
    StaveRecreate();
    // 呼叫 NoteSet()
  });

  if (btnSet) {
    btnSet.addEventListener("click", () => {
      if (!selectedNoteInfo) {
        alert("請先點選一個音符！");
      } else {
        let key = document.getElementById("note-select").value;
        let keyHigh = document.getElementById("pitch-select").value;
        const duration = document.getElementById("duration-select").value;

        if (duration === "休止符/qr") {
          key = "b";
          keyHigh = "4";
        }

        const index = selectedNoteInfo.index;
        const measureIndex = selectedNoteInfo.noteIndex;

        console.log("set key:", key, "set keyHigh:", keyHigh, "set duration:", duration)

        NoteSet(measureIndex, index, key, keyHigh, duration);
      };
    });
  } else {
    console.warn('找不到 <button data-action="Note-Set">');
  };
})


function getMelodyFromMeasure() {
  const melody = [];

  let time = 0;
  for (const group of measure) {
    for (const note of group) {
      const keys = note.getKeys();  // 例如 ["c/4"]
      const duration = note.getDuration(); // 例如 "q", "8", "qr"

      if (duration.endsWith("r")) {
        time += getToneDuration(duration.replace("r", ""));
        continue; // 休止符不播
      }

      const key = keys[0];
      const [pitch, octave] = key.split("/");

      melody.push({
        time: time,
        note: pitch.toUpperCase() + octave,
        duration: getToneDuration(duration),
      });

      time += getToneDuration(duration);
    }
  }

  return melody;
}

function getToneDuration(vexflowDuration) {
  switch (vexflowDuration) {
    case "w": return 4;
    case "h": return 2;
    case "q": return 1;
    case "8": return 0.5;
    case "16": return 0.25;
    default: return 1;
  }
}

async function playScoreMelody() {
  await Tone.start();

  const synth = new Tone.Synth().toDestination();
  const melody = getMelodyFromMeasure();

  // 避免播放重疊
  Tone.Transport.stop();
  Tone.Transport.cancel();
  Tone.Transport.position = 0;

  const part = new Tone.Part((time, value) => {
    synth.triggerAttackRelease(value.note, value.duration, time);
  }, melody).start(0);

  Tone.Transport.start();
}

export { measure, playScoreMelody };