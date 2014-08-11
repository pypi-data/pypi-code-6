import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import gevent.monkey as monkey
monkey.patch_all()

from .trellostats import TrelloStats
from .exceptions import TrelloStatsException

from flask import Flask, request, jsonify, abort
app = Flask(__name__)


@app.route('/api/v1/cycletime', methods=['GET'])
def cycle_time():
    ctx = dict(app_key=request.args.get('app_key'),
               app_token = request.args.get('app_token'),
               board_id = request.args.get('board_id'),
               done = request.args.get('done'))
    assert any(ctx.values())
    logger.info('Recieved request - {}'.format(ctx))
    ts = TrelloStats(ctx)
    try:
        done_id = ts.get_list_id_from_name(ctx.get('done'))
        cards = ts.get_list_data(done_id)
        return jsonify(cycletime=ts.cycle_time(cards))
    except TrelloStatsException:
        abort(500)


def main():
    app.run(debug=True, port=8080, host='localhost')


if __name__ == '__main__':
    main()
