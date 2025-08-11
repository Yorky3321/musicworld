from lib.midi2audio import FluidSynth
import platform
import os
import uuid
from django.core.files.storage import default_storage
from django.http import FileResponse, JsonResponse
from django.conf import settings

def transforming(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    midi_file = request.FILES.get("midi_file")
    if not midi_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    # 暫存 MIDI
    temp_midi_path = default_storage.save(f"temp/{uuid.uuid4()}.mid", midi_file)
    full_midi_path = default_storage.path(temp_midi_path)

    # WAV 輸出路徑
    wav_path = os.path.splitext(temp_midi_path)[0] + ".wav"
    full_wav_path = default_storage.path(wav_path)

    # SoundFont 路徑
    soundfont_path = os.path.join(settings.BASE_DIR, 'Soundfonts', 'GeneralUser-GS.sf2')
    if not os.path.exists(soundfont_path):
        return JsonResponse({"error": "soundfont_path not found"}, status=500)

    if platform.system() == 'Windows':
        fluidsynth_path = r"C:\Users\user\Downloads\bin\fluidsynth.exe"
    else:
        fluidsynth_path = "fluidsynth"  # Linux 下直接呼叫
    # 用 midi2audio 轉檔（不使用 subprocess）
    fs = FluidSynth(sound_font=soundfont_path, fluidsynth_path=fluidsynth_path)
    try:
        print("開始轉檔...")
        fs.midi_to_audio(full_midi_path, full_wav_path)
        print("轉檔結束。")
    except Exception as e:
        return JsonResponse({"error": "Fluidsynth failed", "details": str(e)}, status=500)

    if not os.path.exists(full_wav_path):
        return JsonResponse({"error": "WAV file not created"}, status=500)

    response = FileResponse(open(full_wav_path, "rb"), content_type="audio/wav")
    response["Content-Disposition"] = 'attachment; filename="export.wav"'


    return response
