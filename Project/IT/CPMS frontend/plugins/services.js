import CsService from '@/services/cs'
import DSOService from '@/services/dso'

export default ({ $axios }, inject) => {
  const csService = CsService($axios)
  const dsoService = DSOService($axios)

  inject('services', {
    cs: csService,
    dso: dsoService,
  })
}
