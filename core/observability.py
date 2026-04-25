import os
from dotenv import load_dotenv

load_dotenv()

import litellm
from litellm.integrations.opik.opik import OpikLogger
from opik import configure

# 🔥 configure opik with env
configure(
    api_key=os.getenv("COMET_API_KEY"),
    workspace=os.getenv("COMET_WORKSPACE"),
)

# 🔥 attach opik logger to litellm
litellm.callbacks = [OpikLogger()]