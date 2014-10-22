            try:
                item = self.queue.get(timeout=1)
            except queue.Empty:
                # If we got a timeout, see if we still have runners live. If
                # not, something has gone wrong and we should abort.
                for t in list(live_tasks):
                    if not t.is_alive():
                        live_tasks.remove(t)
                if not live_tasks:
                    break
