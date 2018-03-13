/**
 * Copyright 2017 Intel Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ----------------------------------------------------------------------------
 */
'use strict'

const m = require('mithril')

const api = require('../services/api')
const forms = require('../components/forms')

/**
 * The Form for authorizing an existing user.
 */
const CreateAssetForm = {
  view (vnode) {
    const setter = forms.stateSetter(vnode.state)

    return m('.create-asset-form', [
      m('form', {
        onsubmit: (e) => {
          e.preventDefault()
          const data = {
            name: vnode.state.name,
            description: vnode.state.description,
            owners: [api.getAuth()]
          }
          api.post('assets', data)
            .then(res => {
              console.log(res)
              m.route.set('/assets')
            })
            .catch(api.alertError)
        }
      },
      m('legend', 'Create Asset'),
      forms.textInput(setter('name'), 'Name'),
      forms.textInput(setter('description'), 'Description'),
      m('.form-group',
        m('.row.justify-content-end.align-items-end',
          m('col-2',
            m('button.btn.btn-primary',
              {'data-toggle': 'modal', 'data-target': '#modal'},
              'Create')))))
    ])
  }
}

module.exports = CreateAssetForm
