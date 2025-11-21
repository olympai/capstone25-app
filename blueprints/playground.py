from flask import Blueprint

# BLUEPRINT
playground_bp = Blueprint('playground', __name__, url_prefix='/playground')

# Playground
# load the playground page
@playground_bp.route('/', methods=['GET','POST'])
def b2b_playground():
    # lädt einen playground
    pass

## STREAMING
# start a stream
@playground_bp.route("/start-stream", methods=["POST"])
def start_stream():
    # startet einen stream
    pass

# poll a stream
@playground_bp.route("/get-stream/<task_id>")
def get_stream(task_id):
    pass
    # hier alte get stream funktinalität