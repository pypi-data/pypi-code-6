#coding:utf-8
'''
Created on 18.11.11
@author: akvarats
'''

from m3.ui.actions.async import IBackgroundWorker, AsyncOperationResult

import time


class BackgroundLoader(IBackgroundWorker):

    def start(self):
        # устанавливаем глобальную блокировку процесса
        self.lock()

        # стартуем операцию
        super(BackgroundLoader, self).start()

        # запрашиваем состояние процесса
        alive, _ = self.check_state()

        # формируем результат
        result = AsyncOperationResult(alive=alive)
        return result

    def run(self):

        step = 0
        total = 100
        while step < total:
            alive, _ = self.check_state()
            if not alive:
                break
            self.refresh_state(str(round(1.0 * step/100, 2)))
            time.sleep(0.5)
            step += 1





    def stop(self):
        self.unlock()
        return AsyncOperationResult(alive=False)

    def request(self):

        # запрашиваем состояние процесса
        alive, status_data = self.check_state()
        # формируем результат
        result = AsyncOperationResult(alive=alive)
        try:
            result.value = float(status_data or '')
        except ValueError:
            pass
        return result