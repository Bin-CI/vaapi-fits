###
### Copyright (C) 2021 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ....lib.gstreamer.va.util import *
from ....lib.gstreamer.va.vpp import VppTest

spec = load_test_spec("vpp", "rotation")

@slash.requires(*platform.have_caps("vpp", "rotation"))
class default(VppTest):
  def before(self):
    vars(self).update(
      caps        = platform.get_caps("vpp", "rotation"),
      metric      = dict(type = "md5"),
      vpp_element = "transpose",
    )
    super(default, self).before()

  @slash.parametrize(*gen_vpp_rotation_parameters(spec))
  def test(self, case, degrees):
    vars(self).update(spec[case].copy())
    vars(self).update(
      case      = case,
      degrees   = degrees,
      direction = map_transpose_direction(degrees, None),
      method    = None,
    )

    if self.direction is None:
      slash.skip_test(
        "{degrees} rotation unsupported".format(**vars(self)))

    self.vpp()

  def check_metrics(self):
    self.decoded = self.ofile
    check_metric(**vars(self))
