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

const filterDropdown = (label, assets, setter) => {
  const options = assets.map(asset => ({
    text: asset,
    onclick: setter(asset)
  }))
  options.push({
    text: m('em', 'clear filter'),
    onclick: setter(null)
  })

  return layout.dropdown(label, options, 'success')
}

/**
 * The Form for creating a holding.
 */
const CreateHoldingForm = {
  oninit (vnode) {
    return api.get('assets')
      .then(assets => {
        const publicKey = api.getPublicKey()
        console.log(publicKey, assets)
        vnode.state.assets = assets.reduce((ownedAssets, asset) => {
          if (asset.owners.includes(publicKey)) {
            ownedAssets.push(asset.name)
          }
          return ownedAssets
        }, [])
      })
      .catch(api.ignoreError)
  },

  view (vnode) {
    const assetsOptions = _.get(vnode.state, 'assets', []).map(
      assetName => ({ value: assetName, label: assetName })
    )
    const setter = forms.stateSetter(vnode.state)
    return m('.create-holding-form', [
      m('form', {
        onsubmit: (e) => {
          e.preventDefault()
          const data = {
            label: vnode.state.label,
            description: vnode.state.description,
            asset: vnode.state.asset,
            quantity: +vnode.state.quantity,
          }
          api.post('holdings', data)
            .then(res => {
              console.log(res)
              m.route.set('/offers')
            })
            .catch(api.alertError)
        }
      },
      m('legend', 'Create Holding'),
      forms.textInput(setter('label'), 'Label'),
      forms.textInput(setter('description'), 'Description'),
      forms.select(assetsOptions, setter('asset'), 'Asset' 
      ),
      forms.numberInput(setter('quantity'), 'Quantity'),
      m('.form-group',
        m('.row.justify-content-end.align-items-end',
          m('col-2',
            m('button.btn.btn-primary',
              {'data-toggle': 'modal', 'data-target': '#modal'},
              'Create')))))
    ])
  }
}

module.exports = CreateHoldingForm
