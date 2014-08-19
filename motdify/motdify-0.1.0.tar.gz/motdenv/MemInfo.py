
class MemInfo:
    """ Returns statistics about the memory on the system """

    def getVariableTuple(self):

        with open('/proc/meminfo') as fp:

            meminfo = {}

            for line in fp:
                stat = line.split(':')
                stat_value = int(stat[1].replace(' kB', '').strip())

                # Convert kilobytes to megabytes
                stat_value /= 1000

                meminfo[stat[0]] = stat_value

            return [
                ('MEMORY_TOTAL_MB', meminfo['MemTotal']),
                ('MEMORY_USED_MB', meminfo['MemTotal'] - meminfo['MemFree']),
                ('MEMORY_FREE_MB', meminfo['MemFree']),
                ('SWAP_USED_MB', (meminfo['SwapTotal'] - meminfo['SwapFree']))
            ]