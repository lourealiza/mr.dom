import sys, os
from pathlib import Path

_here = Path(__file__).resolve().parent
_repo = _here.parent
if str(_repo) not in sys.path:
    sys.path.insert(0, str(_repo))

import apirag

def main():
    print('RAW_PATH =', apirag.RAW_PATH)
    print('CHROMA_PATH =', apirag.CHROMA_PATH)
    print('Rebuilding index ...')
    total = apirag.rebuild_index()
    print('Total =', total)
    print('Sample retrieve:')
    print(apirag.retrieve('O que é o DOM360?', k=2))

if __name__ == '__main__':
    main()
