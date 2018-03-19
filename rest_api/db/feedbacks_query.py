# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import rethinkdb as r
from rethinkdb.errors import ReqlNonExistenceError

from api.errors import ApiBadRequest

from db.common import fetch_latest_block_num
from db.common import parse_rules


async def fetch_all_feedback_resources(conn):
    return await r.table('feedbacks')\
        .filter((fetch_latest_block_num() >= r.row['start_block_num'])
                & (fetch_latest_block_num() < r.row['end_block_num']))\
        .map(lambda feedback: (feedback['text'] == "").branch(
            feedback.without('text'), feedback))\
        .without('start_block_num', 'end_block_num', 'delta_id')\
        .coerce_to('array').run(conn)


async def fetch_feedback_resource(conn, asset):
    try:
        return await r.table('feedbacks')\
            .get_all(asset, index='asset')\
            .max('start_block_num')\
            .do(lambda feedback: (feedback['text'] == "").branch(
                feedback.without('text'), feedback))\
            .without('start_block_num', 'end_block_num', 'delta_id')\
            .run(conn)
    except ReqlNonExistenceError:
        raise ApiBadRequest(
            "Bad Request: "
            "No feedback with the asset name {} exists".format(asset))
