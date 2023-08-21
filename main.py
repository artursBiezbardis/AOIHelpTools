import view.view as initView
import os
import helpers.helpers as hellp
from dotenv import load_dotenv

hellp.Helpers().add_to_env('root', os.path.dirname(os.path.abspath(__file__)), '.env')

initView.View().view()
