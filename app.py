"""The conwhordance app.
"""

import pandas
import plotnine
import streamlit

import conwhordance


# %% setup

@streamlit.cache_data
def load_explanation_text(filename):

    return open(filename, encoding='utf-8').read()


def read_uploaded_file(file):

    contents = file.read()

    try:
        text = contents.decode('utf-8')
    except UnicodeDecodeError:
        text = contents.decode('latin-1')

    return text


intro = load_explanation_text('intro.md')
faq = load_explanation_text('FAQ.md')


# %% sidebar

uploaded_files = streamlit.sidebar.file_uploader(
    'upload your story as text files:',
    accept_multiple_files=True,
    help='pick one or more plain text files on your computer (.txt)'
)

pasted_text = streamlit.sidebar.text_area(
    'or paste your text here:',
    help='paste text into the box',
    disabled=bool(uploaded_files)
)

if uploaded_files:
    text = '\n\n'.join(read_uploaded_file(x) for x in uploaded_files)
else:
    text = pasted_text

if text:
    streamlit.sidebar.text_area(
        'your text',
        text[:1000] + '[...]',
        disabled=True
    )


# %% main results field

streamlit.title('conwhordance')
streamlit.markdown(intro)
streamlit.header('your results')

if text:

    corpus = conwhordance.Whorpus(text)
    result = corpus.count()

    if result:

        df = pandas.DataFrame({
            'word': result.keys(),
            'count': result.values()
        })
        df = df.sort_values(['count', 'word'])

        fig = (
            plotnine.ggplot(
                df,
                plotnine.aes(
                    x='word',
                    y='count',
                    label='count'
                )
            )
            + plotnine.scale_x_discrete(
                limits=df['word'].tolist()
            )
            + plotnine.scale_y_continuous(
                breaks=None,
                labels=None
            )
            + plotnine.geom_col()
            + plotnine.geom_text()
            + plotnine.coord_flip()
        )

        streamlit.pyplot(fig.draw())

        for before, whore, after in corpus.concordances():
            streamlit.markdown(f'* {before}**{whore}**{after}')

    else:
        streamlit.markdown('Sorry, you have no *whores*.')

else:

    streamlit.markdown('← *upload or paste your story*')


# %% FAQs

streamlit.subheader('FAQs')
streamlit.markdown(faq)
