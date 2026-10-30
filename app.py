import os, json
import streamlit as st
from checker_fixed import check
st.set_page_config(page_title='MedTransSafe v0.1',page_icon='🩺',layout='wide')
st.title('🩺 MedTransSafe v0.1')
st.caption('Research prototype · English → Urdu medical translation instruction-change detection')
st.warning('Not clinically validated. For research demonstration only. Do not rely on this tool for treatment or medication decisions. Do not enter identifiable patient data.')
with st.sidebar:
    st.header('Configuration')
    key=os.getenv('OPENAI_API_KEY','')
    try: key=key or st.secrets.get('OPENAI_API_KEY','')
    except Exception: pass
    user_key=st.text_input('API key (optional)',type='password',help='If left blank, runs limited non-AI baseline rules. Use hosted secrets for public deployment.')
    key=user_key or key
    model=st.text_input('AI model',value='gpt-4.1-mini')
    verify=st.checkbox('Run independent second verification',value=True)
    st.info('AI mode available' if key else 'Baseline only — configure an API key for AI verification.')
st.subheader('Compare a source instruction and its Urdu translation')
col1,col2=st.columns(2)
with col1: src=st.text_area('English source',value='Do not take this medicine twice daily.',height=160)
with col2: tgt=st.text_area('Urdu translation',value='یہ دوا روزانہ دو بار لیں۔',height=160)
if st.button('Analyze translation',type='primary'):
    try:
        with st.spinner('Analyzing...'):
            result=check(src,tgt,key,model,verify)
        st.session_state['result']=result
    except Exception as e:
        st.error(f'Analysis could not complete: {type(e).__name__}: {str(e)[:250]}')
if 'result' in st.session_state:
    r=st.session_state['result']; st.subheader('Analysis')
    st.write('**Status:**',r['status']);st.write(r['note'])
    for name,label in [('stage1','Stage 1: candidate mismatch detection'),('stage2','Stage 2: independent verification')]:
        stage=r.get(name)
        if stage:
            st.markdown(f'#### {label}')
            st.write('**Verdict:**',stage.get('verdict','uncertain'))
            st.write(stage.get('reason',''))
            if stage.get('flags'): st.dataframe(stage['flags'],use_container_width=True)
            else: st.info('No mismatches flagged; absence of flags does not prove translation safety.')
    st.download_button('Download JSON analysis',json.dumps(r,ensure_ascii=False,indent=2),file_name='medtranssafe_analysis.json',mime='application/json')
with st.expander('Research status and evaluation protocol'):
    st.markdown('''**Implemented:** two sequential AI judgments with separate instructions when configured, lightweight heuristic fallback, disagreement flag, JSON export. **Not established:** diagnostic sensitivity, specificity, inter-rater reliability, clinical readiness, external validation. An independent second call to the same model is not an independent model or a guaranteed reliability gain.\n\n**Next:** construct an expert-labeled subset of the existing English–Urdu corpus, annotate safety-critical semantic changes, blind-review disagreements, calculate precision, recall, F1 and false negative rate for one vs two stages, and report confidence intervals.''')
