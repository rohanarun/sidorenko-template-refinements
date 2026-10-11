"""Version 1.0: execute one reviewed, hash-pinned Python work unit under limits."""
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
import traceback

def main():
    source_path, source_hash, input_path, input_hash, usage_path, cpu, output_cap = sys.argv[1:]
    resource.setrlimit(resource.RLIMIT_CPU, (int(cpu), int(cpu) + 1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (int(output_cap), int(output_cap)))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    source = Path(source_path).read_bytes()
    payload = Path(input_path).read_bytes()
    if hashlib.sha256(source).hexdigest() != source_hash or hashlib.sha256(payload).hexdigest() != input_hash:
        raise RuntimeError('Source or input mutation at execution boundary')
    sys.argv = [source_path, input_path]
    started = time.monotonic()
    code = 0
    try:
        exec(compile(source, source_path, 'exec'), {'__name__': '__main__', '__file__': source_path})
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except BaseException:
        traceback.print_exc()
        code = 1
    finally:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        report = {'exit_code': code, 'wall_seconds': time.monotonic() - started,
                  'user_cpu_seconds': usage.ru_utime, 'system_cpu_seconds': usage.ru_stime,
                  'peak_rss_bytes': usage.ru_maxrss * (1 if sys.platform == 'darwin' else 1024)}
        with open(usage_path, 'x') as f:
            json.dump(report, f, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
    return code

if __name__ == '__main__':
    sys.exit(main())
