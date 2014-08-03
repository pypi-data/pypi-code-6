class TaskType:
    JOB_CREATED = "JOB_CREATED"
    JOB_DELETED = "JOB_DELETED"
    JOB_ADD_MEDIA = "JOB_ADD_MEDIA"
    JOB_ADD_TRANSCRIPT = "JOB_ADD_TRANSCRIPT"
    JOB_PERFORM_TRANSCRIPTION = "JOB_PERFORM_TRANSCRIPTION"
    JOB_PERFORM_PREMIUM_SYNC = "JOB_PERFORM_PREMIUM_SYNC"
    JOB_UPDATE_ELEMENTLIST = "JOB_UPDATE_ELEMENTLIST"
    JOB_GET_TRANSCRIPT = "JOB_GET_TRANSCRIPT"
    JOB_GET_CAPTION = "JOB_GET_CAPTION"
    JOB_GET_ELEMENTLIST = "JOB_GET_ELEMENTLIST"
  

class ErrorType:
    LOGIN_INVALID = "LOGIN_INVALID"
    ACCOUNT_EXISTS = "ACCOUNT_EXISTS"
    ACCOUNT_UNPRIVILEGED = "ACCOUNT_UNPRIVILEGED"
    BAD_API_TOKEN = "BAD_API_TOKEN"
    INVALID_QUERY = "INVALID_QUERY"
    INVALID_OPTION = "INVALID_OPTION"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_URL = "INVALID_URL"
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
  

class JobStatus:
    Authorizing = "SRT"
    Ping = "SRT"
    In_Process = "In Process"
    Complete = "Complete"
  

class TaskStatus:
    COMPLETE = "COMPLETE"
    INPROGRESS = "INPROGRESS"
    ABORTED = "ABORTED"
    FAILED = "FAILED"
  

class Priority:
    ECONOMY = "ECONOMY"
    STANDARD = "STANDARD"
    PRIORITY = "PRIORITY"
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    all = "[ ECONOMY, STANDARD, PRIORITY, CRITICAL, HIGH ]"
  

class Fidelity:
    MECHANICAL = "MECHANICAL"
    STANDARD = "STANDARD"
    HIGH = "HIGH"
    PREMIUM = "PREMIUM"
    PROFESSIONAL = "PROFESSIONAL"
    EXTERNAL = "EXTERNAL"
    all = "[ MECHANICAL, STANDARD, HIGH, PREMIUM, PROFESSIONAL, EXTERNAL ]"
  

class CaptionFormat:
    SRT = "SRT"
    SBV = "SBV"
    DFXP = "DFXP"
    TRANSCRIPT = "TRANSCRIPT"
    TWX = "TWX"
    TPM = "TPM"
    WEB_VTT = "WEB_VTT"
    ECHO = "ECHO"
    all = "[ SRT, SBV, DFXP, QT, TRANSCRIPT, TWX, TPM, WEB_VTT, ECHO ]"
  

class TokenType:
    word = "word"
    punctuation = "punctuation"
    sound = "sound"
  

class Tag:
    S_SENTENCE = "S_SENTENCE"
    UNKNOWN = "UNKNOWN"
    INAUDIBLE = "INAUDIBLE"
    CROSSTALK = "CROSSTALK"
    MUSIC = "MUSIC"
    NOISE = "NOISE"
    LAUGH = "LAUGH"
    COUGH = "COUGH"
    FOREIGN = "FOREIGN"
    GUESSED = "GUESSED"
    BLANK_AUDIO = "BLANK_AUDIO"
    APPLAUSE = "APPLAUSE"
    BLEEP = "BLEEP"
  

class SpeakerId:
    no = "no"
    number = "number"
    name = "name"
  

class SpeakerGer:
    UNKNOWN = "UNKNOWN"
    MALE = "MALE"
    FEMALE = "FEMALE"
  

class Case:
    upper = "upper"
    lower = "lower"
    unchanged = ""
  

class Lineing:
    UNIX = "UNIX"
    WINDOWS = "WINDOWS"
    OSX = "OSX"
  

class CustomerApprovalSteps:
    TRANSLATION = "TRANSLATION"
    RETURN = "RETURN"
  

class CustomerApprovalTools:
    AMARA = "AMARA"
    CIELO24 = "CIELO24"
  

class Language:
    English = "en"
    French = "fr"
    Spanish = "es"
    German = "de"
    Mandarin_Chinese = "cmn"
    Portuguese = "pt"
    Japanese = "jp"
    Arabic = "ar"
    Korean = "ko"
    Traditional_Chinese = "zh"
    Hindi = "hi"
    Italian = "it"
    Russian = "ru"
    Turkish = "tr"
    Hebrew = "he"
    all = "[ en, fr, es, de, cmn, pt, jp, ar, ko, zh, hi, it, ru, tr, he ]"