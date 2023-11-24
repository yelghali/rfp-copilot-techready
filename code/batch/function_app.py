import azure.functions as func
from AddURLEmbeddings import bp_add_url_embeddings
from BatchPushResults import bp_batch_push_results
from BatchStartProcessing import bp_batch_start_processing
from ExtractRFPQuestions import bp_extract_rfp_questions_xlsx

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS) # change to ANONYMOUS for local debugging
app.register_functions(bp_add_url_embeddings)
app.register_functions(bp_batch_push_results)
app.register_functions(bp_batch_start_processing)
app.register_functions(bp_extract_rfp_questions_xlsx)
