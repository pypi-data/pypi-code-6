# SDL_mixer wrapper.
# Part of pysdl2-cffi.

import cffi
import _sdl.cdefs

ffi = cffi.FFI()
ffi.include(_sdl.cdefs.ffi)

# TODO use defines
#define SDL_MIXER_MAJOR_VERSION 2
#define SDL_MIXER_MINOR_VERSION 0
#define SDL_MIXER_PATCHLEVEL    0
#define SDL_MIXER_VERSION(X)                        \
#define MIX_MAJOR_VERSION   SDL_MIXER_MAJOR_VERSION
#define MIX_MINOR_VERSION   SDL_MIXER_MINOR_VERSION
#define MIX_PATCHLEVEL      SDL_MIXER_PATCHLEVEL
#define MIX_VERSION(X)      SDL_MIXER_VERSION(X)

#define Mix_LoadWAV(file)   Mix_LoadWAV_RW(SDL_RWFromFile(file, "rb"), 1)
#define MIX_CHANNEL_POST  -2
#define MIX_EFFECTSMAXSPEED  "MIX_EFFECTSMAXSPEED"
#define Mix_PlayChannel(channel,chunk,loops) Mix_PlayChannelTimed(channel,chunk,loops,-1)
#define Mix_FadeInChannel(channel,chunk,loops,ms) Mix_FadeInChannelTimed(channel,chunk,loops,ms,-1)
#define Mix_SetError    SDL_SetError
#define Mix_GetError    SDL_GetError

ffi.cdef("""
extern int SDL_GetRevisionNumber(void);
extern const SDL_version * Mix_Linked_Version(void);
typedef enum
{
    MIX_INIT_FLAC = 0x00000001,
    MIX_INIT_MOD = 0x00000002,
    MIX_INIT_MODPLUG = 0x00000004,
    MIX_INIT_MP3 = 0x00000008,
    MIX_INIT_OGG = 0x00000010,
    MIX_INIT_FLUIDSYNTH = 0x00000020
} MIX_InitFlags;
extern int Mix_Init(int flags);
extern void Mix_Quit(void);
typedef struct Mix_Chunk {
    int allocated;
    Uint8 *abuf;
    Uint32 alen;
    Uint8 volume;
} Mix_Chunk;
typedef enum {
    MIX_NO_FADING,
    MIX_FADING_OUT,
    MIX_FADING_IN
} Mix_Fading;
typedef enum {
    MUS_NONE,
    MUS_CMD,
    MUS_WAV,
    MUS_MOD,
    MUS_MID,
    MUS_OGG,
    MUS_MP3,
    MUS_MP3_MAD,
    MUS_FLAC,
    MUS_MODPLUG
} Mix_MusicType;
typedef struct _Mix_Music Mix_Music;
extern int Mix_OpenAudio(int frequency, Uint16 format, int channels, int chunksize);
extern int Mix_AllocateChannels(int numchans);
extern int Mix_QuerySpec(int *frequency,Uint16 *format,int *channels);
extern Mix_Chunk * Mix_LoadWAV_RW(SDL_RWops *src, int freesrc);
extern Mix_Music * Mix_LoadMUS(const char *file);
extern Mix_Music * Mix_LoadMUS_RW(SDL_RWops *src, int freesrc);
extern Mix_Music * Mix_LoadMUSType_RW(SDL_RWops *src, Mix_MusicType type, int freesrc);
extern Mix_Chunk * Mix_QuickLoad_WAV(Uint8 *mem);
extern Mix_Chunk * Mix_QuickLoad_RAW(Uint8 *mem, Uint32 len);
extern void Mix_FreeChunk(Mix_Chunk *chunk);
extern void Mix_FreeMusic(Mix_Music *music);
extern int Mix_GetNumChunkDecoders(void);
extern const char * Mix_GetChunkDecoder(int index);
extern int Mix_GetNumMusicDecoders(void);
extern const char * Mix_GetMusicDecoder(int index);
extern Mix_MusicType Mix_GetMusicType(const Mix_Music *music);
extern void Mix_SetPostMix(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg);
extern void Mix_HookMusic(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg);
extern void Mix_HookMusicFinished(void (*music_finished)(void));
extern void * Mix_GetMusicHookData(void);
extern void Mix_ChannelFinished(void (*channel_finished)(int channel));
typedef void (*Mix_EffectFunc_t)(int chan, void *stream, int len, void *udata);
typedef void (*Mix_EffectDone_t)(int chan, void *udata);
extern int Mix_RegisterEffect(int chan, Mix_EffectFunc_t f, Mix_EffectDone_t d, void *arg);
extern int Mix_UnregisterEffect(int channel, Mix_EffectFunc_t f);
extern int Mix_UnregisterAllEffects(int channel);
extern int Mix_SetPanning(int channel, Uint8 left, Uint8 right);
extern int Mix_SetPosition(int channel, Sint16 angle, Uint8 distance);
extern int Mix_SetDistance(int channel, Uint8 distance);
extern int Mix_SetReverseStereo(int channel, int flip);
extern int Mix_ReserveChannels(int num);
extern int Mix_GroupChannel(int which, int tag);
extern int Mix_GroupChannels(int from, int to, int tag);
extern int Mix_GroupAvailable(int tag);
extern int Mix_GroupCount(int tag);
extern int Mix_GroupOldest(int tag);
extern int Mix_GroupNewer(int tag);
extern int Mix_PlayChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ticks);
extern int Mix_PlayMusic(Mix_Music *music, int loops);
extern int Mix_FadeInMusic(Mix_Music *music, int loops, int ms);
extern int Mix_FadeInMusicPos(Mix_Music *music, int loops, int ms, double position);
extern int Mix_FadeInChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ms, int ticks);
extern int Mix_Volume(int channel, int volume);
extern int Mix_VolumeChunk(Mix_Chunk *chunk, int volume);
extern int Mix_VolumeMusic(int volume);
extern int Mix_HaltChannel(int channel);
extern int Mix_HaltGroup(int tag);
extern int Mix_HaltMusic(void);
extern int Mix_ExpireChannel(int channel, int ticks);
extern int Mix_FadeOutChannel(int which, int ms);
extern int Mix_FadeOutGroup(int tag, int ms);
extern int Mix_FadeOutMusic(int ms);
extern Mix_Fading Mix_FadingMusic(void);
extern Mix_Fading Mix_FadingChannel(int which);
extern void Mix_Pause(int channel);
extern void Mix_Resume(int channel);
extern int Mix_Paused(int channel);
extern void Mix_PauseMusic(void);
extern void Mix_ResumeMusic(void);
extern void Mix_RewindMusic(void);
extern int Mix_PausedMusic(void);
extern int Mix_SetMusicPosition(double position);
extern int Mix_Playing(int channel);
extern int Mix_PlayingMusic(void);
extern int Mix_SetMusicCMD(const char *command);
extern int Mix_SetSynchroValue(int value);
extern int Mix_GetSynchroValue(void);
extern int Mix_SetSoundFonts(const char *paths);
extern const char* Mix_GetSoundFonts(void);
extern int Mix_EachSoundFont(int (*function)(const char*, void*), void *data);
extern Mix_Chunk * Mix_GetChunk(int channel);
extern void Mix_CloseAudio(void);
""")


