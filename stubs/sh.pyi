from StringIO import StringIO
from _typeshed import Incomplete
from cStringIO import OutputType as cStringIO
from collections.abc import Generator
from types import ModuleType

__project_url__: str
IS_PY3: Incomplete
MINOR_VER: Incomplete
IS_PY26: Incomplete
ioStringIO = StringIO
iocStringIO = cStringIO

def callable(ob): ...

DEFAULT_ENCODING: Incomplete
IS_MACOS: Incomplete
THIS_DIR: Incomplete
SH_LOGGER_NAME = __name__
RUNNING_TESTS: Incomplete
FORCE_USE_SELECT: Incomplete
PUSHD_LOCK: Incomplete

def get_num_args(fn): ...
raw_input = input
unicode = str
basestring = str
long = int
HAS_POLL: Incomplete
POLLER_EVENT_READ: int
POLLER_EVENT_WRITE: int
POLLER_EVENT_HUP: int
POLLER_EVENT_ERROR: int

class Poller:
    fd_lookup: Incomplete
    fo_lookup: Incomplete
    def __init__(self) -> None: ...
    def __nonzero__(self): ...
    def __len__(self) -> int: ...
    def register_read(self, f) -> None: ...
    def register_write(self, f) -> None: ...
    def register_error(self, f) -> None: ...
    def unregister(self, f) -> None: ...
    def poll(self, timeout): ...

class Poller:
    rlist: Incomplete
    wlist: Incomplete
    xlist: Incomplete
    def __init__(self) -> None: ...
    def __nonzero__(self): ...
    def __len__(self) -> int: ...
    def register_read(self, f) -> None: ...
    def register_write(self, f) -> None: ...
    def register_error(self, f) -> None: ...
    def unregister(self, f) -> None: ...
    def poll(self, timeout): ...

def encode_to_py3bytes_or_py2str(s): ...

class ForkException(Exception):
    def __init__(self, orig_exc) -> None: ...

class ErrorReturnCodeMeta(type):
    def __subclasscheck__(self, o): ...

class ErrorReturnCode(Exception):
    __metaclass__ = ErrorReturnCodeMeta
    truncate_cap: int
    def __reduce__(self): ...
    full_cmd: Incomplete
    stdout: Incomplete
    stderr: Incomplete
    truncate: Incomplete
    def __init__(self, full_cmd, stdout, stderr, truncate: bool = ...) -> None: ...

class SignalException(ErrorReturnCode): ...

class TimeoutException(Exception):
    exit_code: Incomplete
    full_cmd: Incomplete
    def __init__(self, exit_code, full_cmd) -> None: ...

SIGNALS_THAT_SHOULD_THROW_EXCEPTION: Incomplete

class CommandNotFound(AttributeError): ...

rc_exc_regex: Incomplete
rc_exc_cache: Incomplete
SIGNAL_MAPPING: Incomplete

def get_exc_from_name(name): ...
def get_rc_exc(rc): ...

class GlobResults(list):
    path: Incomplete
    def __init__(self, path, results) -> None: ...

def glob(path, *args, **kwargs): ...
def canonicalize(path): ...
def resolve_command_path(program): ...
def resolve_command(name, baked_args: Incomplete | None = ...): ...

class Logger:
    name: Incomplete
    log: Incomplete
    context: Incomplete
    def __init__(self, name, context: Incomplete | None = ...) -> None: ...
    @staticmethod
    def sanitize_context(context): ...
    def get_child(self, name, context): ...
    def info(self, msg, *a) -> None: ...
    def debug(self, msg, *a) -> None: ...
    def error(self, msg, *a) -> None: ...
    def exception(self, msg, *a) -> None: ...

def default_logger_str(cmd, call_args, pid: Incomplete | None = ...): ...

class RunningCommand:
    ran: Incomplete
    call_args: Incomplete
    cmd: Incomplete
    process: Incomplete
    log: Incomplete
    def __init__(self, cmd, call_args, stdin, stdout, stderr) -> None: ...
    def wait(self, timeout: Incomplete | None = ...): ...
    def is_alive(self): ...
    def handle_command_exit_code(self, code) -> None: ...
    @property
    def stdout(self): ...
    @property
    def stderr(self): ...
    @property
    def exit_code(self): ...
    def __len__(self) -> int: ...
    def __enter__(self) -> None: ...
    def __iter__(self): ...
    def next(self): ...
    __next__ = next
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    def __unicode__(self): ...
    def __eq__(self, other): ...
    __hash__: Incomplete
    def __contains__(self, item) -> bool: ...
    def __getattr__(self, p): ...
    def __long__(self): ...
    def __float__(self) -> float: ...
    def __int__(self) -> int: ...

def output_redirect_is_filename(out): ...
def get_prepend_stack(): ...
def special_kwarg_validator(passed_kwargs, merged_kwargs, invalid_list): ...
def get_fileno(ob): ...
def ob_is_fd_based(ob): ...
def ob_is_tty(ob): ...
def ob_is_pipe(ob): ...
def tty_in_validator(passed_kwargs, merged_kwargs): ...
def fg_validator(passed_kwargs, merged_kwargs): ...
def bufsize_validator(passed_kwargs, merged_kwargs): ...
def env_validator(passed_kwargs, merged_kwargs): ...

class Command:
    thread_local: Incomplete
    __name__: Incomplete
    def __init__(self, path, search_paths: Incomplete | None = ...) -> None: ...
    def __getattribute__(self, name): ...
    def bake(self, *args, **kwargs): ...
    def __eq__(self, other): ...
    __hash__: Incomplete
    def __unicode__(self): ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    def __call__(self, *args, **kwargs): ...

def compile_args(a, kwargs, sep, prefix): ...
def aggregate_keywords(keywords, sep, prefix, raw: bool = ...): ...
def setwinsize(fd, rows_cols) -> None: ...
def construct_streamreader_callback(process, handler): ...
def get_exc_exit_code_would_raise(exit_code, ok_codes, sigpipe_ok): ...
def handle_process_exit_code(exit_code): ...
def no_interrupt(syscall, *args, **kwargs): ...

class OProc:
    STDOUT: int
    STDERR: int
    command: Incomplete
    call_args: Incomplete
    ctty: Incomplete
    sid: Incomplete
    pgid: Incomplete
    pid: Incomplete
    timed_out: bool
    started: Incomplete
    cmd: Incomplete
    exit_code: Incomplete
    stdin: Incomplete
    log: Incomplete
    def __init__(self, command, parent_log, cmd, stdin, stdout, stderr, call_args, pipe, process_assign_lock) -> None: ...
    @property
    def output_thread_exc(self): ...
    @property
    def input_thread_exc(self): ...
    @property
    def bg_thread_exc(self): ...
    def change_in_bufsize(self, buf) -> None: ...
    def change_out_bufsize(self, buf) -> None: ...
    def change_err_bufsize(self, buf) -> None: ...
    @property
    def stdout(self): ...
    @property
    def stderr(self): ...
    def get_pgid(self): ...
    def get_sid(self): ...
    def signal_group(self, sig) -> None: ...
    def signal(self, sig) -> None: ...
    def kill_group(self) -> None: ...
    def kill(self) -> None: ...
    def terminate(self) -> None: ...
    def is_alive(self): ...
    def wait(self): ...

def input_thread(log, stdin, is_alive, quit_thread, close_before_term) -> None: ...
def event_wait(ev, timeout: Incomplete | None = ...): ...
def background_thread(timeout_fn, timeout_event, handle_exit_code, is_alive, quit_thread) -> None: ...
def output_thread(log, stdout, stderr, timeout_event, is_alive, quit_thread, stop_output_event) -> None: ...

class DoneReadingForever(Exception): ...
class NotYetReadyToRead(Exception): ...

def determine_how_to_read_input(input_obj): ...
def get_queue_chunk_reader(stdin): ...
def get_callable_chunk_reader(stdin): ...
def get_iter_string_reader(stdin): ...
def get_iter_chunk_reader(stdin): ...
def get_file_chunk_reader(stdin): ...
def bufsize_type_to_bufsize(bf_type): ...

class StreamWriter:
    stream: Incomplete
    stdin: Incomplete
    log: Incomplete
    encoding: Incomplete
    tty_in: Incomplete
    stream_bufferer: Incomplete
    def __init__(self, log, stream, stdin, bufsize_type, encoding, tty_in) -> None: ...
    def fileno(self): ...
    def write(self): ...
    def close(self) -> None: ...

def determine_how_to_feed_output(handler, encoding, decode_errors): ...
def get_fd_chunk_consumer(handler): ...
def get_file_chunk_consumer(handler): ...
def get_callback_chunk_consumer(handler, encoding, decode_errors): ...
def get_cstringio_chunk_consumer(handler): ...
def get_stringio_chunk_consumer(handler, encoding, decode_errors): ...

class StreamReader:
    stream: Incomplete
    buffer: Incomplete
    save_data: Incomplete
    encoding: Incomplete
    decode_errors: Incomplete
    pipe_queue: Incomplete
    log: Incomplete
    stream_bufferer: Incomplete
    bufsize: Incomplete
    should_quit: bool
    def __init__(self, log, stream, handler, buffer, bufsize_type, encoding, decode_errors, pipe_queue: Incomplete | None = ..., save_data: bool = ...) -> None: ...
    def fileno(self): ...
    def close(self) -> None: ...
    def write_chunk(self, chunk) -> None: ...
    def read(self): ...

class StreamBufferer:
    type: Incomplete
    buffer: Incomplete
    n_buffer_count: int
    encoding: Incomplete
    decode_errors: Incomplete
    log: Incomplete
    def __init__(self, buffer_type, encoding=..., decode_errors: str = ...) -> None: ...
    def change_buffering(self, new_type) -> None: ...
    def process(self, chunk): ...
    def flush(self): ...

def with_lock(lock): ...
def pushd(path) -> Generator[None, None, None]: ...

class Environment(dict):
    whitelist: Incomplete
    globs: Incomplete
    baked_args: Incomplete
    def __init__(self, globs, baked_args: Incomplete | None = ...) -> None: ...
    def __getitem__(self, k): ...
    @staticmethod
    def b_which(program, paths: Incomplete | None = ...): ...

class Cd:
    def __new__(cls, path: Incomplete | None = ...): ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

class Contrib(ModuleType):
    @classmethod
    def __call__(cls, name): ...

mod_name: Incomplete
contrib: Incomplete

def git(orig): ...
def sudo(*args: str) -> RunningCommand: ...
def bash(*args: str) -> RunningCommand: ...
def ssh(orig): ...
def run_repl(env) -> None: ...

class SelfWrapper(ModuleType):
    __path__: Incomplete
    def __init__(self, self_module, baked_args: Incomplete | None = ...) -> None: ...
    def __getattr__(self, name): ...
    def __call__(self, **kwargs): ...

def in_importlib(frame): ...
def register_importer(): ...
def fetch_module_from_frame(name, frame): ...

class ModuleImporterFromVariables:
    restrict_to: Incomplete
    def __init__(self, restrict_to: Incomplete | None = ...) -> None: ...
    def find_module(self, mod_fullname, path: Incomplete | None = ...): ...
    def find_spec(self, fullname, path: Incomplete | None = ..., target: Incomplete | None = ...): ...
    def load_module(self, mod_fullname): ...
