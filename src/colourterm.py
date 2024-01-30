from typing import Optional
from ctypes import wintypes, windll
import ctypes

class NullValueException(Exception):
  def __init__(self, message: str):
    self.message = message
    self.code = ctypes.get_last_error()

  def get_message(self):
    return f"Error: {self.message} with error code {self.code}"


class ColourTerm():
  
  STD_OUTPUT_HANDLE: wintypes.DWORD = 4294967285   # Gets the stdout handle to the current window.
  ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004      # Enables coloured text.
  
  ALL_DEFAULT =         "\x1b[0m"
  
  F_BLACK =             "\x1b[30m"
  F_RED =               "\x1b[31m"
  F_GREEN =             "\x1b[32m"
  F_YELLOW =            "\x1b[33m"
  F_BLUE =              "\x1b[34m"
  F_MAGENTA =           "\x1b[35m"
  F_CYAN =              "\x1b[36m"
  F_WHITE =             "\x1b[37m"
  F_EXT =               "\x1b[38m"
  F_DEFAULT =           "\x1b[39m"
  
  B_BLACK =             "\x1b[40m"
  B_RED =               "\x1b[41m"
  B_GREEN =             "\x1b[42m"
  B_YELLOW =            "\x1b[43m"
  B_BLUE =              "\x1b[44m"
  B_MAGENTA =           "\x1b[45m"
  B_CYAN =              "\x1b[46m"
  B_WHITE =             "\x1b[47m"
  B_EXT =               "\x1b[48m"
  B_DEFAULT =           "\x1b[49m"
  
  BR_F_BLACK =          "\x1b[90m"
  BR_F_RED =            "\x1b[91m"
  BR_F_GREEN =          "\x1b[92m"
  BR_F_YELLOW =         "\x1b[93m"
  BR_F_BLUE =           "\x1b[94m"
  BR_F_MAGENTA =        "\x1b[95m"
  BR_F_CYAN =           "\x1b[96m"
  BR_F_WHITE =          "\x1b[97m"
  BR_B_BLACK =          "\x1b[100m"
  BR_B_RED =            "\x1b[101m"
  BR_B_GREEN =          "\x1b[102m"
  BR_B_YELLOW =         "\x1b[103m"
  BR_B_BLUE =           "\x1b[104m"
  BR_B_MAGENTA =        "\x1b[105m"
  BR_B_CYAN =           "\x1b[106m"
  BR_B_WHITE =          "\x1b[107m"


  def fd_black(text: str) -> str:
    return f"{ColourTerm.F_BLACK}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_red(text: str) -> str:
    return f"{ColourTerm.F_RED}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_green(text: str) -> str:
    return f"{ColourTerm.F_GREEN}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_yellow(text: str) -> str:
    return f"{ColourTerm.F_YELLOW}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_blue(text: str) -> str:
    return f"{ColourTerm.F_BLUE}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_magenta(text: str) -> str:
    return f"{ColourTerm.F_MAGENTA}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_cyan(text: str) -> str:
    return f"{ColourTerm.F_CYAN}{text}{ColourTerm.ALL_DEFAULT}"


  def fd_white(text: str) -> str:
    return f"{ColourTerm.F_WHITE}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_black(text: str) -> str:
    return f"{ColourTerm.B_BLACK}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_red(text: str) -> str:
    return f"{ColourTerm.B_RED}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_green(text: str) -> str:
    return f"{ColourTerm.B_GREEN}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_yellow(text: str) -> str:
    return f"{ColourTerm.B_YELLOW}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_blue(text: str) -> str:
    return f"{ColourTerm.B_BLUE}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_magenta(text: str) -> str:
    return f"{ColourTerm.B_MAGENTA}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_cyan(text: str) -> str:
    return f"{ColourTerm.B_CYAN}{text}{ColourTerm.ALL_DEFAULT}"


  def bd_white(text: str) -> str:
    return f"{ColourTerm.B_WHITE}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_black(text: str) -> str:
    return f"{ColourTerm.BR_F_BLACK}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_red(text: str) -> str:
    return f"{ColourTerm.BR_F_RED}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def f_green(text: str) -> str:
    return f"{ColourTerm.BR_F_GREEN}{text}{ColourTerm.ALL_DEFAULT}"


  def f_yellow(text: str) -> str:
    return f"{ColourTerm.BR_F_YELLOW}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_blue(text: str) -> str:
    return f"{ColourTerm.BR_F_BLUE}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_magenta(text: str) -> str:
    return f"{ColourTerm.BR_F_MAGENTA}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_cyan(text: str) -> str:
    return f"{ColourTerm.BR_F_CYAN}{text}{ColourTerm.ALL_DEFAULT}"
  

  def f_white(text: str) -> str:
    return f"{ColourTerm.BR_F_WHITE}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_black(text: str) -> str:
    return f"{ColourTerm.BR_B_BLACK}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_red(text: str) -> str:
    return f"{ColourTerm.BR_B_RED}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_green(text: str) -> str:
    return f"{ColourTerm.BR_B_GREEN}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_yellow(text: str) -> str:
    return f"{ColourTerm.BR_B_YELLOW}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_blue(text: str) -> str:
    return f"{ColourTerm.BR_B_BLUE}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_magenta(text: str) -> str:
    return f"{ColourTerm.BR_B_MAGENTA}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_cyan(text: str) -> str:
    return f"{ColourTerm.BR_B_CYAN}{text}{ColourTerm.ALL_DEFAULT}"
  
  
  def b_white(text: str) -> str:
    return f"{ColourTerm.BR_B_WHITE}{text}{ColourTerm.ALL_DEFAULT}"

  
  def __set_console_mode(hConsoleHandle: wintypes.HANDLE, dwMode: wintypes.DWORD) -> bool:
    '''Functions sets the mode of the current console window.'''
    
    SetConsoleMode = windll.kernel32.SetConsoleMode     # Gets the function ptr.
    SetConsoleMode.restype = wintypes.BOOL              # Sets the return type.

    SetConsoleMode.argtypes = (  # Defines the function arguments.
      wintypes.HANDLE,           # _In_ HANDLE hConsoleHandle
      wintypes.DWORD             # _In_ DWORD dwMode
    )
    
    success: wintypes.BOOL = SetConsoleMode(hConsoleHandle, dwMode)
    return bool(success)


  def __get_console_mode(hConsoleHandle: wintypes.HANDLE, lpMode: Optional[wintypes.DWORD]) -> bool:
    '''Gets the mode of the current console window.'''
    
    GetConsoleMode = windll.kernel32.GetConsoleMode     # Gets the function ptr.
    GetConsoleMode.restype = wintypes.BOOL              # Sets the return type.

    GetConsoleMode.argtypes = ( # Defines the function arguments.
      wintypes.HANDLE,          # _In_ hConsoleHandle  HANDLE
      wintypes.LPDWORD,         # _Out_ lpMode LPDWORD
    )

    # Calls function as passes lpMode in as a '&lpMode' reference.
    success: wintypes.BOOL = GetConsoleMode(hConsoleHandle, ctypes.byref(lpMode))
    return bool(success)


  def __get_std_handle(nStdHandle: wintypes.DWORD) -> wintypes.HANDLE:
    GetStdHandle = windll.kernel32.GetStdHandle # Grabs the pointer to the GetStdHandle function in kernel32.dll
    GetStdHandle.restype = wintypes.HANDLE      # Sets the return type to a win32 Handle.

    GetStdHandle.argtypes = (  # Defines the function arguments.
      wintypes.DWORD,          # _In_ DWORD nStdHandle
    )

    stdout: Optional[wintypes.HANDLE] = None
    stdout = GetStdHandle(nStdHandle)

    # Return none if the handle is NULL
    if stdout == None:
      raise NullValueException("Failed to get valid stdout handle")
    
    return stdout


  def enable_colour_terminal() -> bool:
    stdout: Optional[wintypes.HANDLE] = None

    # Attempt to get a valid handle of the current console window.
    try:
      stdout = ColourTerm.__get_std_handle(ColourTerm.STD_OUTPUT_HANDLE)
    except NullValueException("Failed to get a win32 hamdle to current console window") as e:
      print(e)
      return False
    
    # Get the mode of the current console window.
    mode: wintypes.DWORD = wintypes.DWORD(0)
    success = ColourTerm.__get_console_mode(stdout, mode)
    
    if success == False:
      print("Info: Failed to get the current console mode")

    # Perform an xor operation on the mode and the VIRTUAL_TERMINAL_PROCESSING values.
    mode = wintypes.DWORD(mode.value ^ ColourTerm.ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    success = ColourTerm.__set_console_mode(stdout, mode)

    if success == False:
      print(f"Failed to enable colour terminal with error code: {ctypes.get_last_error()}")

    return success