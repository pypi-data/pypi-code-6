# API
import apipkg

exports = ['ADDEVENT',
 'ALPHA_OPAQUE',
 'ALPHA_TRANSPARENT',
 'APP_DIDENTERBACKGROUND',
 'APP_DIDENTERFOREGROUND',
 'APP_LOWMEMORY',
 'APP_TERMINATING',
 'APP_WILLENTERBACKGROUND',
 'APP_WILLENTERFOREGROUND',
 'ARRAYORDER_ABGR',
 'ARRAYORDER_ARGB',
 'ARRAYORDER_BGR',
 'ARRAYORDER_BGRA',
 'ARRAYORDER_NONE',
 'ARRAYORDER_RGB',
 'ARRAYORDER_RGBA',
 'ASSEMBLY_ROUTINES',
 'ASSERTION_ABORT',
 'ASSERTION_ALWAYS_IGNORE',
 'ASSERTION_BREAK',
 'ASSERTION_IGNORE',
 'ASSERTION_RETRY',
 'ASSERT_LEVEL',
 'AUDIO_DRIVER_ALSA',
 'AUDIO_DRIVER_ALSA_DYNAMIC',
 'AUDIO_DRIVER_DISK',
 'AUDIO_DRIVER_DUMMY',
 'AUDIO_DRIVER_OSS',
 'AUDIO_DRIVER_PULSEAUDIO',
 'AUDIO_DRIVER_PULSEAUDIO_DYNAMIC',
 'AUDIO_PAUSED',
 'AUDIO_PLAYING',
 'AUDIO_STOPPED',
 'AudioCVT',
 'AudioSpec',
 'BITMAPORDER_1234',
 'BITMAPORDER_4321',
 'BITMAPORDER_NONE',
 'BITSPERPIXEL',
 'BLENDMODE_ADD',
 'BLENDMODE_BLEND',
 'BLENDMODE_MOD',
 'BLENDMODE_NONE',
 'BUTTON_LEFT',
 'BUTTON_LMASK',
 'BUTTON_MIDDLE',
 'BUTTON_MMASK',
 'BUTTON_RIGHT',
 'BUTTON_RMASK',
 'BUTTON_X1',
 'BUTTON_X1MASK',
 'BUTTON_X2',
 'BUTTON_X2MASK',
 'BYTESPERPIXEL',
 'CLIPBOARDUPDATE',
 'COMPILEDVERSION',
 'CONTROLLERAXISMOTION',
 'CONTROLLERBUTTONDOWN',
 'CONTROLLERBUTTONUP',
 'CONTROLLERDEVICEADDED',
 'CONTROLLERDEVICEREMAPPED',
 'CONTROLLERDEVICEREMOVED',
 'CONTROLLER_AXIS_INVALID',
 'CONTROLLER_AXIS_LEFTX',
 'CONTROLLER_AXIS_LEFTY',
 'CONTROLLER_AXIS_MAX',
 'CONTROLLER_AXIS_RIGHTX',
 'CONTROLLER_AXIS_RIGHTY',
 'CONTROLLER_AXIS_TRIGGERLEFT',
 'CONTROLLER_AXIS_TRIGGERRIGHT',
 'CONTROLLER_BINDTYPE_AXIS',
 'CONTROLLER_BINDTYPE_BUTTON',
 'CONTROLLER_BINDTYPE_HAT',
 'CONTROLLER_BINDTYPE_NONE',
 'CONTROLLER_BUTTON_A',
 'CONTROLLER_BUTTON_B',
 'CONTROLLER_BUTTON_BACK',
 'CONTROLLER_BUTTON_DPAD_DOWN',
 'CONTROLLER_BUTTON_DPAD_LEFT',
 'CONTROLLER_BUTTON_DPAD_RIGHT',
 'CONTROLLER_BUTTON_DPAD_UP',
 'CONTROLLER_BUTTON_GUIDE',
 'CONTROLLER_BUTTON_INVALID',
 'CONTROLLER_BUTTON_LEFTSHOULDER',
 'CONTROLLER_BUTTON_LEFTSTICK',
 'CONTROLLER_BUTTON_MAX',
 'CONTROLLER_BUTTON_RIGHTSHOULDER',
 'CONTROLLER_BUTTON_RIGHTSTICK',
 'CONTROLLER_BUTTON_START',
 'CONTROLLER_BUTTON_X',
 'CONTROLLER_BUTTON_Y',
 'Color',
 'CommonEvent',
 'ControllerAxisEvent',
 'ControllerButtonEvent',
 'ControllerDeviceEvent',
 'Cursor',
 'DEFINE_PIXELFORMAT',
 'DEFINE_PIXELFOURCC',
 'DISABLE',
 'DOLLARGESTURE',
 'DOLLARRECORD',
 'DONTFREE',
 'DROPFILE',
 'DisplayMode',
 'DollarGestureEvent',
 'DropEvent',
 'EFREAD',
 'EFSEEK',
 'EFWRITE',
 'ENABLE',
 'ENOMEM',
 'Event',
 'FALSE',
 'FILE',
 'FILESYSTEM_UNIX',
 'FINGERDOWN',
 'FINGERMOTION',
 'FINGERUP',
 'FIRSTEVENT',
 'FLIP_HORIZONTAL',
 'FLIP_NONE',
 'FLIP_VERTICAL',
 'FOURCC',
 'FUNCTION',
 'Finger',
 'GETEVENT',
 'GL_ACCELERATED_VISUAL',
 'GL_ACCUM_ALPHA_SIZE',
 'GL_ACCUM_BLUE_SIZE',
 'GL_ACCUM_GREEN_SIZE',
 'GL_ACCUM_RED_SIZE',
 'GL_ALPHA_SIZE',
 'GL_BLUE_SIZE',
 'GL_BUFFER_SIZE',
 'GL_BindTexture',
 'GL_CONTEXT_DEBUG_FLAG',
 'GL_CONTEXT_EGL',
 'GL_CONTEXT_FLAGS',
 'GL_CONTEXT_FORWARD_COMPATIBLE_FLAG',
 'GL_CONTEXT_MAJOR_VERSION',
 'GL_CONTEXT_MINOR_VERSION',
 'GL_CONTEXT_PROFILE_COMPATIBILITY',
 'GL_CONTEXT_PROFILE_CORE',
 'GL_CONTEXT_PROFILE_ES',
 'GL_CONTEXT_PROFILE_MASK',
 'GL_CONTEXT_RESET_ISOLATION_FLAG',
 'GL_CONTEXT_ROBUST_ACCESS_FLAG',
 'GL_CreateContext',
 'GL_DEPTH_SIZE',
 'GL_DOUBLEBUFFER',
 'GL_DeleteContext',
 'GL_ExtensionSupported',
 'GL_FRAMEBUFFER_SRGB_CAPABLE',
 'GL_GREEN_SIZE',
 'GL_GetAttribute',
 'GL_GetCurrentContext',
 'GL_GetCurrentWindow',
 'GL_GetProcAddress',
 'GL_GetSwapInterval',
 'GL_LoadLibrary',
 'GL_MULTISAMPLEBUFFERS',
 'GL_MULTISAMPLESAMPLES',
 'GL_MakeCurrent',
 'GL_RED_SIZE',
 'GL_RETAINED_BACKING',
 'GL_SHARE_WITH_CURRENT_CONTEXT',
 'GL_STENCIL_SIZE',
 'GL_STEREO',
 'GL_SetAttribute',
 'GL_SetSwapInterval',
 'GL_SwapWindow',
 'GL_UnbindTexture',
 'GL_UnloadLibrary',
 'GameController',
 'GameControllerButtonBind',
 'HAPTIC_AUTOCENTER',
 'HAPTIC_CARTESIAN',
 'HAPTIC_CONSTANT',
 'HAPTIC_CUSTOM',
 'HAPTIC_DAMPER',
 'HAPTIC_FRICTION',
 'HAPTIC_GAIN',
 'HAPTIC_INERTIA',
 'HAPTIC_INFINITY',
 'HAPTIC_LEFTRIGHT',
 'HAPTIC_LINUX',
 'HAPTIC_PAUSE',
 'HAPTIC_POLAR',
 'HAPTIC_RAMP',
 'HAPTIC_SAWTOOTHDOWN',
 'HAPTIC_SAWTOOTHUP',
 'HAPTIC_SINE',
 'HAPTIC_SPHERICAL',
 'HAPTIC_SPRING',
 'HAPTIC_STATUS',
 'HAPTIC_TRIANGLE',
 'HAT_CENTERED',
 'HAT_DOWN',
 'HAT_LEFT',
 'HAT_LEFTDOWN',
 'HAT_LEFTUP',
 'HAT_RIGHT',
 'HAT_RIGHTDOWN',
 'HAT_RIGHTUP',
 'HAT_UP',
 'HINT_ACCELEROMETER_AS_JOYSTICK',
 'HINT_ALLOW_TOPMOST',
 'HINT_DEFAULT',
 'HINT_FRAMEBUFFER_ACCELERATION',
 'HINT_GAMECONTROLLERCONFIG',
 'HINT_GRAB_KEYBOARD',
 'HINT_IDLE_TIMER_DISABLED',
 'HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS',
 'HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK',
 'HINT_MOUSE_RELATIVE_MODE_WARP',
 'HINT_NORMAL',
 'HINT_ORIENTATIONS',
 'HINT_OVERRIDE',
 'HINT_RENDER_DIRECT3D11_DEBUG',
 'HINT_RENDER_DIRECT3D_THREADSAFE',
 'HINT_RENDER_DRIVER',
 'HINT_RENDER_OPENGL_SHADERS',
 'HINT_RENDER_SCALE_QUALITY',
 'HINT_RENDER_VSYNC',
 'HINT_TIMER_RESOLUTION',
 'HINT_VIDEO_ALLOW_SCREENSAVER',
 'HINT_VIDEO_HIGHDPI_DISABLED',
 'HINT_VIDEO_MAC_FULLSCREEN_SPACES',
 'HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS',
 'HINT_VIDEO_WINDOW_SHARE_PIXEL_FORMAT',
 'HINT_VIDEO_WIN_D3DCOMPILER',
 'HINT_VIDEO_X11_XINERAMA',
 'HINT_VIDEO_X11_XRANDR',
 'HINT_VIDEO_X11_XVIDMODE',
 'HINT_WINRT_HANDLE_BACK_BUTTON',
 'HINT_WINRT_PRIVACY_POLICY_LABEL',
 'HINT_WINRT_PRIVACY_POLICY_URL',
 'HINT_XINPUT_ENABLED',
 'Haptic',
 'HapticCondition',
 'HapticConstant',
 'HapticCustom',
 'HapticDirection',
 'HapticEffect',
 'HapticLeftRight',
 'HapticPeriodic',
 'HapticRamp',
 'IGNORE',
 'INIT_AUDIO',
 'INIT_EVENTS',
 'INIT_EVERYTHING',
 'INIT_GAMECONTROLLER',
 'INIT_HAPTIC',
 'INIT_JOYSTICK',
 'INIT_NOPARACHUTE',
 'INIT_TIMER',
 'INIT_VIDEO',
 'INPUT_LINUXEV',
 'INPUT_LINUXKD',
 'ISPIXELFORMAT_ALPHA',
 'ISPIXELFORMAT_FOURCC',
 'ISPIXELFORMAT_INDEXED',
 'JOYAXISMOTION',
 'JOYBALLMOTION',
 'JOYBUTTONDOWN',
 'JOYBUTTONUP',
 'JOYDEVICEADDED',
 'JOYDEVICEREMOVED',
 'JOYHATMOTION',
 'JOYSTICK_LINUX',
 'JoyAxisEvent',
 'JoyBallEvent',
 'JoyButtonEvent',
 'JoyDeviceEvent',
 'JoyHatEvent',
 'Joystick',
 'JoystickGUID',
 'KEYDOWN',
 'KEYUP',
 'KMOD_CAPS',
 'KMOD_LALT',
 'KMOD_LCTRL',
 'KMOD_LGUI',
 'KMOD_LSHIFT',
 'KMOD_MODE',
 'KMOD_NONE',
 'KMOD_NUM',
 'KMOD_RALT',
 'KMOD_RCTRL',
 'KMOD_RESERVED',
 'KMOD_RGUI',
 'KMOD_RSHIFT',
 'K_0',
 'K_1',
 'K_2',
 'K_3',
 'K_4',
 'K_5',
 'K_6',
 'K_7',
 'K_8',
 'K_9',
 'K_AC_BACK',
 'K_AC_BOOKMARKS',
 'K_AC_FORWARD',
 'K_AC_HOME',
 'K_AC_REFRESH',
 'K_AC_SEARCH',
 'K_AC_STOP',
 'K_AGAIN',
 'K_ALTERASE',
 'K_AMPERSAND',
 'K_APPLICATION',
 'K_ASTERISK',
 'K_AT',
 'K_AUDIOMUTE',
 'K_AUDIONEXT',
 'K_AUDIOPLAY',
 'K_AUDIOPREV',
 'K_AUDIOSTOP',
 'K_BACKQUOTE',
 'K_BACKSLASH',
 'K_BACKSPACE',
 'K_BRIGHTNESSDOWN',
 'K_BRIGHTNESSUP',
 'K_CALCULATOR',
 'K_CANCEL',
 'K_CAPSLOCK',
 'K_CARET',
 'K_CLEAR',
 'K_CLEARAGAIN',
 'K_COLON',
 'K_COMMA',
 'K_COMPUTER',
 'K_COPY',
 'K_CRSEL',
 'K_CURRENCYSUBUNIT',
 'K_CURRENCYUNIT',
 'K_CUT',
 'K_DECIMALSEPARATOR',
 'K_DELETE',
 'K_DISPLAYSWITCH',
 'K_DOLLAR',
 'K_DOWN',
 'K_EJECT',
 'K_END',
 'K_EQUALS',
 'K_ESCAPE',
 'K_EXCLAIM',
 'K_EXECUTE',
 'K_EXSEL',
 'K_F1',
 'K_F10',
 'K_F11',
 'K_F12',
 'K_F13',
 'K_F14',
 'K_F15',
 'K_F16',
 'K_F17',
 'K_F18',
 'K_F19',
 'K_F2',
 'K_F20',
 'K_F21',
 'K_F22',
 'K_F23',
 'K_F24',
 'K_F3',
 'K_F4',
 'K_F5',
 'K_F6',
 'K_F7',
 'K_F8',
 'K_F9',
 'K_FIND',
 'K_GREATER',
 'K_HASH',
 'K_HELP',
 'K_HOME',
 'K_INSERT',
 'K_KBDILLUMDOWN',
 'K_KBDILLUMTOGGLE',
 'K_KBDILLUMUP',
 'K_KP_0',
 'K_KP_00',
 'K_KP_000',
 'K_KP_1',
 'K_KP_2',
 'K_KP_3',
 'K_KP_4',
 'K_KP_5',
 'K_KP_6',
 'K_KP_7',
 'K_KP_8',
 'K_KP_9',
 'K_KP_A',
 'K_KP_AMPERSAND',
 'K_KP_AT',
 'K_KP_B',
 'K_KP_BACKSPACE',
 'K_KP_BINARY',
 'K_KP_C',
 'K_KP_CLEAR',
 'K_KP_CLEARENTRY',
 'K_KP_COLON',
 'K_KP_COMMA',
 'K_KP_D',
 'K_KP_DBLAMPERSAND',
 'K_KP_DBLVERTICALBAR',
 'K_KP_DECIMAL',
 'K_KP_DIVIDE',
 'K_KP_E',
 'K_KP_ENTER',
 'K_KP_EQUALS',
 'K_KP_EQUALSAS400',
 'K_KP_EXCLAM',
 'K_KP_F',
 'K_KP_GREATER',
 'K_KP_HASH',
 'K_KP_HEXADECIMAL',
 'K_KP_LEFTBRACE',
 'K_KP_LEFTPAREN',
 'K_KP_LESS',
 'K_KP_MEMADD',
 'K_KP_MEMCLEAR',
 'K_KP_MEMDIVIDE',
 'K_KP_MEMMULTIPLY',
 'K_KP_MEMRECALL',
 'K_KP_MEMSTORE',
 'K_KP_MEMSUBTRACT',
 'K_KP_MINUS',
 'K_KP_MULTIPLY',
 'K_KP_OCTAL',
 'K_KP_PERCENT',
 'K_KP_PERIOD',
 'K_KP_PLUS',
 'K_KP_PLUSMINUS',
 'K_KP_POWER',
 'K_KP_RIGHTBRACE',
 'K_KP_RIGHTPAREN',
 'K_KP_SPACE',
 'K_KP_TAB',
 'K_KP_VERTICALBAR',
 'K_KP_XOR',
 'K_LALT',
 'K_LCTRL',
 'K_LEFT',
 'K_LEFTBRACKET',
 'K_LEFTPAREN',
 'K_LESS',
 'K_LGUI',
 'K_LSHIFT',
 'K_MAIL',
 'K_MEDIASELECT',
 'K_MENU',
 'K_MINUS',
 'K_MODE',
 'K_MUTE',
 'K_NUMLOCKCLEAR',
 'K_OPER',
 'K_OUT',
 'K_PAGEDOWN',
 'K_PAGEUP',
 'K_PASTE',
 'K_PAUSE',
 'K_PERCENT',
 'K_PERIOD',
 'K_PLUS',
 'K_POWER',
 'K_PRINTSCREEN',
 'K_PRIOR',
 'K_QUESTION',
 'K_QUOTE',
 'K_QUOTEDBL',
 'K_RALT',
 'K_RCTRL',
 'K_RETURN',
 'K_RETURN2',
 'K_RGUI',
 'K_RIGHT',
 'K_RIGHTBRACKET',
 'K_RIGHTPAREN',
 'K_RSHIFT',
 'K_SCANCODE_MASK',
 'K_SCROLLLOCK',
 'K_SELECT',
 'K_SEMICOLON',
 'K_SEPARATOR',
 'K_SLASH',
 'K_SLEEP',
 'K_SPACE',
 'K_STOP',
 'K_SYSREQ',
 'K_TAB',
 'K_THOUSANDSSEPARATOR',
 'K_UNDERSCORE',
 'K_UNDO',
 'K_UNKNOWN',
 'K_UP',
 'K_VOLUMEDOWN',
 'K_VOLUMEUP',
 'K_WWW',
 'K_a',
 'K_b',
 'K_c',
 'K_d',
 'K_e',
 'K_f',
 'K_g',
 'K_h',
 'K_i',
 'K_j',
 'K_k',
 'K_l',
 'K_m',
 'K_n',
 'K_o',
 'K_p',
 'K_q',
 'K_r',
 'K_s',
 'K_t',
 'K_u',
 'K_v',
 'K_w',
 'K_x',
 'K_y',
 'K_z',
 'KeyboardEvent',
 'Keysym',
 'LASTERROR',
 'LASTEVENT',
 'LINE',
 'LOADSO_DLOPEN',
 'LOG_CATEGORY_APPLICATION',
 'LOG_CATEGORY_ASSERT',
 'LOG_CATEGORY_AUDIO',
 'LOG_CATEGORY_CUSTOM',
 'LOG_CATEGORY_ERROR',
 'LOG_CATEGORY_INPUT',
 'LOG_CATEGORY_RENDER',
 'LOG_CATEGORY_RESERVED1',
 'LOG_CATEGORY_RESERVED10',
 'LOG_CATEGORY_RESERVED2',
 'LOG_CATEGORY_RESERVED3',
 'LOG_CATEGORY_RESERVED4',
 'LOG_CATEGORY_RESERVED5',
 'LOG_CATEGORY_RESERVED6',
 'LOG_CATEGORY_RESERVED7',
 'LOG_CATEGORY_RESERVED8',
 'LOG_CATEGORY_RESERVED9',
 'LOG_CATEGORY_SYSTEM',
 'LOG_CATEGORY_TEST',
 'LOG_CATEGORY_VIDEO',
 'LOG_PRIORITY_CRITICAL',
 'LOG_PRIORITY_DEBUG',
 'LOG_PRIORITY_ERROR',
 'LOG_PRIORITY_INFO',
 'LOG_PRIORITY_VERBOSE',
 'LOG_PRIORITY_WARN',
 'MAJOR_VERSION',
 'MAX_LOG_MESSAGE',
 'MESSAGEBOX_BUTTON_ESCAPEKEY_DEFAULT',
 'MESSAGEBOX_BUTTON_RETURNKEY_DEFAULT',
 'MESSAGEBOX_COLOR_BACKGROUND',
 'MESSAGEBOX_COLOR_BUTTON_BACKGROUND',
 'MESSAGEBOX_COLOR_BUTTON_BORDER',
 'MESSAGEBOX_COLOR_BUTTON_SELECTED',
 'MESSAGEBOX_COLOR_MAX',
 'MESSAGEBOX_COLOR_TEXT',
 'MESSAGEBOX_ERROR',
 'MESSAGEBOX_INFORMATION',
 'MESSAGEBOX_WARNING',
 'MINOR_VERSION',
 'MOUSEBUTTONDOWN',
 'MOUSEBUTTONUP',
 'MOUSEMOTION',
 'MOUSEWHEEL',
 'MULTIGESTURE',
 'MessageBoxButtonData',
 'MessageBoxColor',
 'MessageBoxColorScheme',
 'MessageBoxData',
 'MouseButtonEvent',
 'MouseMotionEvent',
 'MouseWheelEvent',
 'MultiGestureEvent',
 'NULL_WHILE_LOOP_CONDITION',
 'NUM_LOG_PRIORITIES',
 'NUM_SCANCODES',
 'NUM_SYSTEM_CURSORS',
 'OSEvent',
 'PACKEDLAYOUT_1010102',
 'PACKEDLAYOUT_1555',
 'PACKEDLAYOUT_2101010',
 'PACKEDLAYOUT_332',
 'PACKEDLAYOUT_4444',
 'PACKEDLAYOUT_5551',
 'PACKEDLAYOUT_565',
 'PACKEDLAYOUT_8888',
 'PACKEDLAYOUT_NONE',
 'PACKEDORDER_ABGR',
 'PACKEDORDER_ARGB',
 'PACKEDORDER_BGRA',
 'PACKEDORDER_BGRX',
 'PACKEDORDER_NONE',
 'PACKEDORDER_RGBA',
 'PACKEDORDER_RGBX',
 'PACKEDORDER_XBGR',
 'PACKEDORDER_XRGB',
 'PATCHLEVEL',
 'PEEKEVENT',
 'PIXELFLAG',
 'PIXELFORMAT_ABGR1555',
 'PIXELFORMAT_ABGR4444',
 'PIXELFORMAT_ABGR8888',
 'PIXELFORMAT_ARGB1555',
 'PIXELFORMAT_ARGB2101010',
 'PIXELFORMAT_ARGB4444',
 'PIXELFORMAT_ARGB8888',
 'PIXELFORMAT_BGR24',
 'PIXELFORMAT_BGR555',
 'PIXELFORMAT_BGR565',
 'PIXELFORMAT_BGR888',
 'PIXELFORMAT_BGRA4444',
 'PIXELFORMAT_BGRA5551',
 'PIXELFORMAT_BGRA8888',
 'PIXELFORMAT_BGRX8888',
 'PIXELFORMAT_INDEX1LSB',
 'PIXELFORMAT_INDEX1MSB',
 'PIXELFORMAT_INDEX4LSB',
 'PIXELFORMAT_INDEX4MSB',
 'PIXELFORMAT_INDEX8',
 'PIXELFORMAT_IYUV',
 'PIXELFORMAT_RGB24',
 'PIXELFORMAT_RGB332',
 'PIXELFORMAT_RGB444',
 'PIXELFORMAT_RGB555',
 'PIXELFORMAT_RGB565',
 'PIXELFORMAT_RGB888',
 'PIXELFORMAT_RGBA4444',
 'PIXELFORMAT_RGBA5551',
 'PIXELFORMAT_RGBA8888',
 'PIXELFORMAT_RGBX8888',
 'PIXELFORMAT_UNKNOWN',
 'PIXELFORMAT_UYVY',
 'PIXELFORMAT_YUY2',
 'PIXELFORMAT_YV12',
 'PIXELFORMAT_YVYU',
 'PIXELLAYOUT',
 'PIXELORDER',
 'PIXELTYPE',
 'PIXELTYPE_ARRAYF16',
 'PIXELTYPE_ARRAYF32',
 'PIXELTYPE_ARRAYU16',
 'PIXELTYPE_ARRAYU32',
 'PIXELTYPE_ARRAYU8',
 'PIXELTYPE_INDEX1',
 'PIXELTYPE_INDEX4',
 'PIXELTYPE_INDEX8',
 'PIXELTYPE_PACKED16',
 'PIXELTYPE_PACKED32',
 'PIXELTYPE_PACKED8',
 'PIXELTYPE_UNKNOWN',
 'POWERSTATE_CHARGED',
 'POWERSTATE_CHARGING',
 'POWERSTATE_NO_BATTERY',
 'POWERSTATE_ON_BATTERY',
 'POWERSTATE_UNKNOWN',
 'POWER_LINUX',
 'PREALLOC',
 'PRESSED',
 'Palette',
 'PixelFormat',
 'Point',
 'QUERY',
 'QUIT',
 'QuitEvent',
 'RELEASED',
 'RENDERER_ACCELERATED',
 'RENDERER_PRESENTVSYNC',
 'RENDERER_SOFTWARE',
 'RENDERER_TARGETTEXTURE',
 'RENDER_DEVICE_RESET',
 'RENDER_TARGETS_RESET',
 'RLEACCEL',
 'RWFromConstMem',
 'RWFromFP',
 'RWFromFile',
 'RWFromMem',
 'RWOPS_JNIFILE',
 'RWOPS_MEMORY',
 'RWOPS_MEMORY_RO',
 'RWOPS_STDFILE',
 'RWOPS_UNKNOWN',
 'RWOPS_WINFILE',
 'RWops',
 'Rect',
 'Renderer',
 'RendererInfo',
 'SCANCODE_0',
 'SCANCODE_1',
 'SCANCODE_2',
 'SCANCODE_3',
 'SCANCODE_4',
 'SCANCODE_5',
 'SCANCODE_6',
 'SCANCODE_7',
 'SCANCODE_8',
 'SCANCODE_9',
 'SCANCODE_A',
 'SCANCODE_AC_BACK',
 'SCANCODE_AC_BOOKMARKS',
 'SCANCODE_AC_FORWARD',
 'SCANCODE_AC_HOME',
 'SCANCODE_AC_REFRESH',
 'SCANCODE_AC_SEARCH',
 'SCANCODE_AC_STOP',
 'SCANCODE_AGAIN',
 'SCANCODE_ALTERASE',
 'SCANCODE_APOSTROPHE',
 'SCANCODE_APP1',
 'SCANCODE_APP2',
 'SCANCODE_APPLICATION',
 'SCANCODE_AUDIOMUTE',
 'SCANCODE_AUDIONEXT',
 'SCANCODE_AUDIOPLAY',
 'SCANCODE_AUDIOPREV',
 'SCANCODE_AUDIOSTOP',
 'SCANCODE_B',
 'SCANCODE_BACKSLASH',
 'SCANCODE_BACKSPACE',
 'SCANCODE_BRIGHTNESSDOWN',
 'SCANCODE_BRIGHTNESSUP',
 'SCANCODE_C',
 'SCANCODE_CALCULATOR',
 'SCANCODE_CANCEL',
 'SCANCODE_CAPSLOCK',
 'SCANCODE_CLEAR',
 'SCANCODE_CLEARAGAIN',
 'SCANCODE_COMMA',
 'SCANCODE_COMPUTER',
 'SCANCODE_COPY',
 'SCANCODE_CRSEL',
 'SCANCODE_CURRENCYSUBUNIT',
 'SCANCODE_CURRENCYUNIT',
 'SCANCODE_CUT',
 'SCANCODE_D',
 'SCANCODE_DECIMALSEPARATOR',
 'SCANCODE_DELETE',
 'SCANCODE_DISPLAYSWITCH',
 'SCANCODE_DOWN',
 'SCANCODE_E',
 'SCANCODE_EJECT',
 'SCANCODE_END',
 'SCANCODE_EQUALS',
 'SCANCODE_ESCAPE',
 'SCANCODE_EXECUTE',
 'SCANCODE_EXSEL',
 'SCANCODE_F',
 'SCANCODE_F1',
 'SCANCODE_F10',
 'SCANCODE_F11',
 'SCANCODE_F12',
 'SCANCODE_F13',
 'SCANCODE_F14',
 'SCANCODE_F15',
 'SCANCODE_F16',
 'SCANCODE_F17',
 'SCANCODE_F18',
 'SCANCODE_F19',
 'SCANCODE_F2',
 'SCANCODE_F20',
 'SCANCODE_F21',
 'SCANCODE_F22',
 'SCANCODE_F23',
 'SCANCODE_F24',
 'SCANCODE_F3',
 'SCANCODE_F4',
 'SCANCODE_F5',
 'SCANCODE_F6',
 'SCANCODE_F7',
 'SCANCODE_F8',
 'SCANCODE_F9',
 'SCANCODE_FIND',
 'SCANCODE_G',
 'SCANCODE_GRAVE',
 'SCANCODE_H',
 'SCANCODE_HELP',
 'SCANCODE_HOME',
 'SCANCODE_I',
 'SCANCODE_INSERT',
 'SCANCODE_INTERNATIONAL1',
 'SCANCODE_INTERNATIONAL2',
 'SCANCODE_INTERNATIONAL3',
 'SCANCODE_INTERNATIONAL4',
 'SCANCODE_INTERNATIONAL5',
 'SCANCODE_INTERNATIONAL6',
 'SCANCODE_INTERNATIONAL7',
 'SCANCODE_INTERNATIONAL8',
 'SCANCODE_INTERNATIONAL9',
 'SCANCODE_J',
 'SCANCODE_K',
 'SCANCODE_KBDILLUMDOWN',
 'SCANCODE_KBDILLUMTOGGLE',
 'SCANCODE_KBDILLUMUP',
 'SCANCODE_KP_0',
 'SCANCODE_KP_00',
 'SCANCODE_KP_000',
 'SCANCODE_KP_1',
 'SCANCODE_KP_2',
 'SCANCODE_KP_3',
 'SCANCODE_KP_4',
 'SCANCODE_KP_5',
 'SCANCODE_KP_6',
 'SCANCODE_KP_7',
 'SCANCODE_KP_8',
 'SCANCODE_KP_9',
 'SCANCODE_KP_A',
 'SCANCODE_KP_AMPERSAND',
 'SCANCODE_KP_AT',
 'SCANCODE_KP_B',
 'SCANCODE_KP_BACKSPACE',
 'SCANCODE_KP_BINARY',
 'SCANCODE_KP_C',
 'SCANCODE_KP_CLEAR',
 'SCANCODE_KP_CLEARENTRY',
 'SCANCODE_KP_COLON',
 'SCANCODE_KP_COMMA',
 'SCANCODE_KP_D',
 'SCANCODE_KP_DBLAMPERSAND',
 'SCANCODE_KP_DBLVERTICALBAR',
 'SCANCODE_KP_DECIMAL',
 'SCANCODE_KP_DIVIDE',
 'SCANCODE_KP_E',
 'SCANCODE_KP_ENTER',
 'SCANCODE_KP_EQUALS',
 'SCANCODE_KP_EQUALSAS400',
 'SCANCODE_KP_EXCLAM',
 'SCANCODE_KP_F',
 'SCANCODE_KP_GREATER',
 'SCANCODE_KP_HASH',
 'SCANCODE_KP_HEXADECIMAL',
 'SCANCODE_KP_LEFTBRACE',
 'SCANCODE_KP_LEFTPAREN',
 'SCANCODE_KP_LESS',
 'SCANCODE_KP_MEMADD',
 'SCANCODE_KP_MEMCLEAR',
 'SCANCODE_KP_MEMDIVIDE',
 'SCANCODE_KP_MEMMULTIPLY',
 'SCANCODE_KP_MEMRECALL',
 'SCANCODE_KP_MEMSTORE',
 'SCANCODE_KP_MEMSUBTRACT',
 'SCANCODE_KP_MINUS',
 'SCANCODE_KP_MULTIPLY',
 'SCANCODE_KP_OCTAL',
 'SCANCODE_KP_PERCENT',
 'SCANCODE_KP_PERIOD',
 'SCANCODE_KP_PLUS',
 'SCANCODE_KP_PLUSMINUS',
 'SCANCODE_KP_POWER',
 'SCANCODE_KP_RIGHTBRACE',
 'SCANCODE_KP_RIGHTPAREN',
 'SCANCODE_KP_SPACE',
 'SCANCODE_KP_TAB',
 'SCANCODE_KP_VERTICALBAR',
 'SCANCODE_KP_XOR',
 'SCANCODE_L',
 'SCANCODE_LALT',
 'SCANCODE_LANG1',
 'SCANCODE_LANG2',
 'SCANCODE_LANG3',
 'SCANCODE_LANG4',
 'SCANCODE_LANG5',
 'SCANCODE_LANG6',
 'SCANCODE_LANG7',
 'SCANCODE_LANG8',
 'SCANCODE_LANG9',
 'SCANCODE_LCTRL',
 'SCANCODE_LEFT',
 'SCANCODE_LEFTBRACKET',
 'SCANCODE_LGUI',
 'SCANCODE_LSHIFT',
 'SCANCODE_M',
 'SCANCODE_MAIL',
 'SCANCODE_MEDIASELECT',
 'SCANCODE_MENU',
 'SCANCODE_MINUS',
 'SCANCODE_MODE',
 'SCANCODE_MUTE',
 'SCANCODE_N',
 'SCANCODE_NONUSBACKSLASH',
 'SCANCODE_NONUSHASH',
 'SCANCODE_NUMLOCKCLEAR',
 'SCANCODE_O',
 'SCANCODE_OPER',
 'SCANCODE_OUT',
 'SCANCODE_P',
 'SCANCODE_PAGEDOWN',
 'SCANCODE_PAGEUP',
 'SCANCODE_PASTE',
 'SCANCODE_PAUSE',
 'SCANCODE_PERIOD',
 'SCANCODE_POWER',
 'SCANCODE_PRINTSCREEN',
 'SCANCODE_PRIOR',
 'SCANCODE_Q',
 'SCANCODE_R',
 'SCANCODE_RALT',
 'SCANCODE_RCTRL',
 'SCANCODE_RETURN',
 'SCANCODE_RETURN2',
 'SCANCODE_RGUI',
 'SCANCODE_RIGHT',
 'SCANCODE_RIGHTBRACKET',
 'SCANCODE_RSHIFT',
 'SCANCODE_S',
 'SCANCODE_SCROLLLOCK',
 'SCANCODE_SELECT',
 'SCANCODE_SEMICOLON',
 'SCANCODE_SEPARATOR',
 'SCANCODE_SLASH',
 'SCANCODE_SLEEP',
 'SCANCODE_SPACE',
 'SCANCODE_STOP',
 'SCANCODE_SYSREQ',
 'SCANCODE_T',
 'SCANCODE_TAB',
 'SCANCODE_THOUSANDSSEPARATOR',
 'SCANCODE_U',
 'SCANCODE_UNDO',
 'SCANCODE_UNKNOWN',
 'SCANCODE_UP',
 'SCANCODE_V',
 'SCANCODE_VOLUMEDOWN',
 'SCANCODE_VOLUMEUP',
 'SCANCODE_W',
 'SCANCODE_WWW',
 'SCANCODE_X',
 'SCANCODE_Y',
 'SCANCODE_Z',
 'SDLError',
 'SWSURFACE',
 'SYSTEM_CURSOR_ARROW',
 'SYSTEM_CURSOR_CROSSHAIR',
 'SYSTEM_CURSOR_HAND',
 'SYSTEM_CURSOR_IBEAM',
 'SYSTEM_CURSOR_NO',
 'SYSTEM_CURSOR_SIZEALL',
 'SYSTEM_CURSOR_SIZENESW',
 'SYSTEM_CURSOR_SIZENS',
 'SYSTEM_CURSOR_SIZENWSE',
 'SYSTEM_CURSOR_SIZEWE',
 'SYSTEM_CURSOR_WAIT',
 'SYSTEM_CURSOR_WAITARROW',
 'SYSWMEVENT',
 'Struct',
 'Surface',
 'SysWMEvent',
 'SysWMmsg',
 'TEXTEDITING',
 'TEXTEDITINGEVENT_TEXT_SIZE',
 'TEXTINPUT',
 'TEXTINPUTEVENT_TEXT_SIZE',
 'TEXTUREACCESS_STATIC',
 'TEXTUREACCESS_STREAMING',
 'TEXTUREACCESS_TARGET',
 'TEXTUREMODULATE_ALPHA',
 'TEXTUREMODULATE_COLOR',
 'TEXTUREMODULATE_NONE',
 'THREAD_PRIORITY_HIGH',
 'THREAD_PRIORITY_LOW',
 'THREAD_PRIORITY_NORMAL',
 'THREAD_PTHREAD',
 'THREAD_PTHREAD_RECURSIVE_MUTEX',
 'TIMER_UNIX',
 'TLSCreate',
 'TLSGet',
 'TLSSet',
 'TOUCH_MOUSEID',
 'TRUE',
 'TextEditingEvent',
 'TextInputEvent',
 'Texture',
 'Thread',
 'TouchFingerEvent',
 'UNSUPPORTED',
 'USEREVENT',
 'UserEvent',
 'VIDEO_DRIVER_DUMMY',
 'VIDEO_DRIVER_X11',
 'VIDEO_DRIVER_X11_CONST_PARAM_XDATA32',
 'VIDEO_DRIVER_X11_CONST_PARAM_XEXTADDDISPLAY',
 'VIDEO_DRIVER_X11_DYNAMIC',
 'VIDEO_DRIVER_X11_DYNAMIC_XCURSOR',
 'VIDEO_DRIVER_X11_DYNAMIC_XEXT',
 'VIDEO_DRIVER_X11_DYNAMIC_XINERAMA',
 'VIDEO_DRIVER_X11_DYNAMIC_XINPUT2',
 'VIDEO_DRIVER_X11_DYNAMIC_XRANDR',
 'VIDEO_DRIVER_X11_DYNAMIC_XSS',
 'VIDEO_DRIVER_X11_DYNAMIC_XVIDMODE',
 'VIDEO_DRIVER_X11_HAS_XKBKEYCODETOKEYSYM',
 'VIDEO_DRIVER_X11_SUPPORTS_GENERIC_EVENTS',
 'VIDEO_DRIVER_X11_XCURSOR',
 'VIDEO_DRIVER_X11_XINERAMA',
 'VIDEO_DRIVER_X11_XINPUT2',
 'VIDEO_DRIVER_X11_XINPUT2_SUPPORTS_MULTITOUCH',
 'VIDEO_DRIVER_X11_XRANDR',
 'VIDEO_DRIVER_X11_XSCRNSAVER',
 'VIDEO_DRIVER_X11_XSHAPE',
 'VIDEO_DRIVER_X11_XVIDMODE',
 'VIDEO_OPENGL',
 'VIDEO_OPENGL_GLX',
 'VIDEO_RENDER_OGL',
 'WINDOWEVENT',
 'WINDOWEVENT_CLOSE',
 'WINDOWEVENT_ENTER',
 'WINDOWEVENT_EXPOSED',
 'WINDOWEVENT_FOCUS_GAINED',
 'WINDOWEVENT_FOCUS_LOST',
 'WINDOWEVENT_HIDDEN',
 'WINDOWEVENT_LEAVE',
 'WINDOWEVENT_MAXIMIZED',
 'WINDOWEVENT_MINIMIZED',
 'WINDOWEVENT_MOVED',
 'WINDOWEVENT_NONE',
 'WINDOWEVENT_RESIZED',
 'WINDOWEVENT_RESTORED',
 'WINDOWEVENT_SHOWN',
 'WINDOWEVENT_SIZE_CHANGED',
 'WINDOWPOS_CENTERED',
 'WINDOWPOS_CENTERED_MASK',
 'WINDOWPOS_UNDEFINED',
 'WINDOWPOS_UNDEFINED_MASK',
 'WINDOW_ALLOW_HIGHDPI',
 'WINDOW_BORDERLESS',
 'WINDOW_FOREIGN',
 'WINDOW_FULLSCREEN',
 'WINDOW_FULLSCREEN_DESKTOP',
 'WINDOW_HIDDEN',
 'WINDOW_INPUT_FOCUS',
 'WINDOW_INPUT_GRABBED',
 'WINDOW_MAXIMIZED',
 'WINDOW_MINIMIZED',
 'WINDOW_MOUSE_FOCUS',
 'WINDOW_OPENGL',
 'WINDOW_RESIZABLE',
 'WINDOW_SHOWN',
 'Window',
 'WindowEvent',
 'abs',
 'absolute_import',
 'addEventWatch',
 'addHintCallback',
 'addTimer',
 'allocFormat',
 'allocPalette',
 'allocRW',
 'assert_data',
 'atan',
 'atan2',
 'atof',
 'atoi',
 'atomicLock',
 'atomicTryLock',
 'atomicUnlock',
 'atomic_t',
 'audioInit',
 'audioQuit',
 'blitSurface',
 'buildAudioCVT',
 'calculateGammaRamp',
 'calloc',
 'ceil',
 'clearError',
 'clearHints',
 'closeAudio',
 'closeAudioDevice',
 'cond',
 'condBroadcast',
 'condSignal',
 'condWait',
 'condWaitTimeout',
 'convertAudio',
 'convertPixels',
 'convertSurface',
 'convertSurfaceFormat',
 'copysign',
 'cos',
 'cosf',
 'createColorCursor',
 'createCond',
 'createCursor',
 'createMutex',
 'createRGBSurface',
 'createRGBSurfaceFrom',
 'createRenderer',
 'createSemaphore',
 'createSoftwareRenderer',
 'createSystemCursor',
 'createTexture',
 'createTextureFromSurface',
 'createThread',
 'createWindow',
 'createWindowAndRenderer',
 'createWindowFrom',
 'delEventWatch',
 'delHintCallback',
 'delay',
 'destroyCond',
 'destroyMutex',
 'destroyRenderer',
 'destroySemaphore',
 'destroyTexture',
 'destroyWindow',
 'disableScreenSaver',
 'enableScreenSaver',
 'enclosePoints',
 'error',
 'eventState',
 'fabs',
 'ffi',
 'fillRect',
 'fillRects',
 'filterEvents',
 'floor',
 'flushEvent',
 'flushEvents',
 'free',
 'freeCursor',
 'freeFormat',
 'freePalette',
 'freeRW',
 'freeSurface',
 'freeWAV',
 'gameControllerAddMapping',
 'gameControllerClose',
 'gameControllerEventState',
 'gameControllerGetAttached',
 'gameControllerGetAxis',
 'gameControllerGetAxisFromString',
 'gameControllerGetBindForAxis',
 'gameControllerGetBindForButton',
 'gameControllerGetButton',
 'gameControllerGetButtonFromString',
 'gameControllerGetJoystick',
 'gameControllerGetStringForAxis',
 'gameControllerGetStringForButton',
 'gameControllerMapping',
 'gameControllerMappingForGUID',
 'gameControllerName',
 'gameControllerNameForIndex',
 'gameControllerOpen',
 'gameControllerUpdate',
 'getAssertionReport',
 'getAudioDeviceName',
 'getAudioDeviceStatus',
 'getAudioDriver',
 'getAudioStatus',
 'getCPUCacheLineSize',
 'getCPUCount',
 'getClipRect',
 'getClipboardText',
 'getClosestDisplayMode',
 'getColorKey',
 'getCurrentAudioDriver',
 'getCurrentDisplayMode',
 'getCurrentVideoDriver',
 'getCursor',
 'getDefaultCursor',
 'getDesktopDisplayMode',
 'getDisplayBounds',
 'getDisplayMode',
 'getDisplayName',
 'getError',
 'getEventFilter',
 'getHint',
 'getKeyFromName',
 'getKeyFromScancode',
 'getKeyName',
 'getKeyboardFocus',
 'getKeyboardState',
 'getModState',
 'getMouseFocus',
 'getMouseState',
 'getNumAudioDevices',
 'getNumAudioDrivers',
 'getNumDisplayModes',
 'getNumRenderDrivers',
 'getNumTouchDevices',
 'getNumTouchFingers',
 'getNumVideoDisplays',
 'getNumVideoDrivers',
 'getPerformanceCounter',
 'getPerformanceFrequency',
 'getPixelFormatName',
 'getPlatform',
 'getPowerInfo',
 'getRGB',
 'getRGBA',
 'getRelativeMouseMode',
 'getRelativeMouseState',
 'getRenderDrawBlendMode',
 'getRenderDrawColor',
 'getRenderDriverInfo',
 'getRenderTarget',
 'getRenderer',
 'getRendererInfo',
 'getRendererOutputSize',
 'getRevision',
 'getRevisionNumber',
 'getScancodeFromKey',
 'getScancodeFromName',
 'getScancodeName',
 'getSurfaceAlphaMod',
 'getSurfaceBlendMode',
 'getSurfaceColorMod',
 'getTextureAlphaMod',
 'getTextureBlendMode',
 'getTextureColorMod',
 'getThreadID',
 'getThreadName',
 'getTicks',
 'getTouchDevice',
 'getTouchFinger',
 'getVersion',
 'getVideoDriver',
 'getWindowBrightness',
 'getWindowData',
 'getWindowDisplayIndex',
 'getWindowDisplayMode',
 'getWindowFlags',
 'getWindowFromID',
 'getWindowGammaRamp',
 'getWindowGrab',
 'getWindowID',
 'getWindowMaximumSize',
 'getWindowMinimumSize',
 'getWindowPixelFormat',
 'getWindowPosition',
 'getWindowSize',
 'getWindowSurface',
 'getWindowTitle',
 'getenv',
 'hapticClose',
 'hapticDestroyEffect',
 'hapticEffectSupported',
 'hapticGetEffectStatus',
 'hapticIndex',
 'hapticName',
 'hapticNewEffect',
 'hapticNumAxes',
 'hapticNumEffects',
 'hapticNumEffectsPlaying',
 'hapticOpen',
 'hapticOpenFromJoystick',
 'hapticOpenFromMouse',
 'hapticOpened',
 'hapticPause',
 'hapticQuery',
 'hapticRumbleInit',
 'hapticRumblePlay',
 'hapticRumbleStop',
 'hapticRumbleSupported',
 'hapticRunEffect',
 'hapticSetAutocenter',
 'hapticSetGain',
 'hapticStopAll',
 'hapticStopEffect',
 'hapticUnpause',
 'hapticUpdateEffect',
 'has3DNow',
 'hasAltiVec',
 'hasClipboardText',
 'hasEvent',
 'hasEvents',
 'hasIntersection',
 'hasMMX',
 'hasRDTSC',
 'hasSSE',
 'hasSSE2',
 'hasSSE3',
 'hasSSE41',
 'hasSSE42',
 'hasScreenKeyboardSupport',
 'hideWindow',
 'iconv',
 'iconv_close',
 'iconv_open',
 'iconv_string',
 'init',
 'initSubSystem',
 'intersectRect',
 'intersectRectAndLine',
 'isGameController',
 'isScreenKeyboardShown',
 'isScreenSaverEnabled',
 'isTextInputActive',
 'isdigit',
 'isspace',
 'itoa',
 'joystickClose',
 'joystickEventState',
 'joystickGetAttached',
 'joystickGetAxis',
 'joystickGetBall',
 'joystickGetButton',
 'joystickGetDeviceGUID',
 'joystickGetGUID',
 'joystickGetGUIDFromString',
 'joystickGetGUIDString',
 'joystickGetHat',
 'joystickInstanceID',
 'joystickIsHaptic',
 'joystickName',
 'joystickNameForIndex',
 'joystickNumAxes',
 'joystickNumBalls',
 'joystickNumButtons',
 'joystickNumHats',
 'joystickOpen',
 'joystickUpdate',
 'lib',
 'lltoa',
 'loadBMP_RW',
 'loadDollarTemplates',
 'loadFunction',
 'loadObject',
 'loadWAV_RW',
 'lockAudio',
 'lockAudioDevice',
 'lockMutex',
 'lockSurface',
 'lockTexture',
 'log',
 'logCritical',
 'logDebug',
 'logError',
 'logGetOutputFunction',
 'logGetPriority',
 'logInfo',
 'logMessage',
 'logMessageV',
 'logResetPriorities',
 'logSetAllPriority',
 'logSetOutputFunction',
 'logSetPriority',
 'logVerbose',
 'logWarn',
 'lowerBlit',
 'lowerBlitScaled',
 'ltoa',
 'main',
 'malloc',
 'mapRGB',
 'mapRGBA',
 'masksToPixelFormatEnum',
 'maximizeWindow',
 'memcmp',
 'memcpy',
 'memmove',
 'memset',
 'minimizeWindow',
 'mixAudio',
 'mixAudioFormat',
 'mouseIsHaptic',
 'mutex',
 'numHaptics',
 'numJoysticks',
 'openAudio',
 'openAudioDevice',
 'pauseAudio',
 'pauseAudioDevice',
 'peepEvents',
 'pixelFormatEnumToMasks',
 'pollEvent',
 'pow',
 'pumpEvents',
 'pushEvent',
 'qsort',
 'queryTexture',
 'quit',
 'quitSubSystem',
 'raiseWindow',
 'readBE16',
 'readBE32',
 'readBE64',
 'readLE16',
 'readLE32',
 'readLE64',
 'readU8',
 'realloc',
 'recordGesture',
 'registerEvents',
 'removeTimer',
 'renderClear',
 'renderCopy',
 'renderCopyEx',
 'renderDrawLine',
 'renderDrawLines',
 'renderDrawPoint',
 'renderDrawPoints',
 'renderDrawRect',
 'renderDrawRects',
 'renderFillRect',
 'renderFillRects',
 'renderGetClipRect',
 'renderGetLogicalSize',
 'renderGetScale',
 'renderGetViewport',
 'renderPresent',
 'renderReadPixels',
 'renderSetClipRect',
 'renderSetLogicalSize',
 'renderSetScale',
 'renderSetViewport',
 'renderTargetSupported',
 'reportAssertion',
 'resetAssertionReport',
 'restoreWindow',
 'saveAllDollarTemplates',
 'saveBMP_RW',
 'saveDollarTemplate',
 'scalbn',
 'sem',
 'semPost',
 'semTryWait',
 'semValue',
 'semWait',
 'semWaitTimeout',
 'setAssertionHandler',
 'setClipRect',
 'setClipboardText',
 'setColorKey',
 'setCursor',
 'setError',
 'setEventFilter',
 'setHint',
 'setHintWithPriority',
 'setMainReady',
 'setModState',
 'setPaletteColors',
 'setPixelFormatPalette',
 'setRelativeMouseMode',
 'setRenderDrawBlendMode',
 'setRenderDrawColor',
 'setRenderTarget',
 'setSurfaceAlphaMod',
 'setSurfaceBlendMode',
 'setSurfaceColorMod',
 'setSurfacePalette',
 'setSurfaceRLE',
 'setTextInputRect',
 'setTextureAlphaMod',
 'setTextureBlendMode',
 'setTextureColorMod',
 'setThreadPriority',
 'setWindowBordered',
 'setWindowBrightness',
 'setWindowData',
 'setWindowDisplayMode',
 'setWindowFullscreen',
 'setWindowGammaRamp',
 'setWindowGrab',
 'setWindowIcon',
 'setWindowMaximumSize',
 'setWindowMinimumSize',
 'setWindowPosition',
 'setWindowSize',
 'setWindowTitle',
 'setenv',
 'showCursor',
 'showMessageBox',
 'showSimpleMessageBox',
 'showWindow',
 'sin',
 'sinf',
 'snprintf',
 'softStretch',
 'sqrt',
 'sscanf',
 'startTextInput',
 'stopTextInput',
 'strcasecmp',
 'strchr',
 'strcmp',
 'strdup',
 'strlcat',
 'strlcpy',
 'strlen',
 'strlwr',
 'strncasecmp',
 'strncmp',
 'strrchr',
 'strrev',
 'strstr',
 'strtod',
 'strtol',
 'strtoll',
 'strtoul',
 'strtoull',
 'strupr',
 'threadID',
 'tolower',
 'toupper',
 'tryLockMutex',
 'uitoa',
 'ulltoa',
 'ultoa',
 'unionRect',
 'unloadObject',
 'unlockAudio',
 'unlockAudioDevice',
 'unlockMutex',
 'unlockSurface',
 'unlockTexture',
 'updateTexture',
 'updateWindowSurface',
 'updateWindowSurfaceRects',
 'upperBlit',
 'upperBlitScaled',
 'utf8strlcpy',
 'version',
 'videoInit',
 'videoQuit',
 'vsnprintf',
 'waitEvent',
 'waitEventTimeout',
 'waitThread',
 'warpMouseInWindow',
 'wasInit',
 'wcslcat',
 'wcslcpy',
 'wcslen',
 'writeBE16',
 'writeBE32',
 'writeBE64',
 'writeLE16',
 'writeLE32',
 'writeLE64',
 'writeU8']

ns_dict = dict((s, '_sdl.renamed:%s' % s)
               for s in exports if not s.startswith('_'))
ns_dict['image'] = '_sdl_image.renamed'
ns_dict['mixer'] = '_sdl_mixer.renamed'
ns_dict['ttf'] = '_sdl_ttf.renamed'

apipkg.initpkg(__name__, ns_dict, {'__all__':exports})
