import sys, os
import pandas as pd
from specter import Spec, expect
from timezone import Timezone
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'code'))

class TimezoneSpec(Spec):
    class to_standard(Spec):
        def should_convert_to_standard(self):
            tz = Timezone('Abu Dhabi')
            expect(tz.to_standard()).to.equal('Asia/Muscat')
