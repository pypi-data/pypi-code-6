class ParseIdMixin(object):
    def _parse_tx_ids(self, tx_ids):
        parsed_ids = []
        for tx_id in tx_ids.split(','):
            if '-' in tx_id:
                tx_id_range = tx_id.split('-')
                assert len(tx_id_range) == 2

                beg = int(tx_id_range[0])
                end = int(tx_id_range[1]) + 1
                parsed_ids.extend([x for x in range(beg, end)])
            else:
                parsed_ids.append(int(tx_id))
        # Remove duplicates by converting to a set and back
        return list(set(parsed_ids))
