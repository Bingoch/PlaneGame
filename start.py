# _*_ coding=utf-8 _*_
import traceback

from bin.Main import main

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()