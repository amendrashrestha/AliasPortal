from flask import Flask, render_template, request, jsonify

import pandas as pd
import traceback
import sys
import os

from langdetect import detect

import warnings
warnings.filterwarnings("ignore")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.append(APP_ROOT)

import IOReadWrite as IO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route("/predict")
def predict():
    text1 = request.args.get('text1').strip()
    text2 = request.args.get('text2').strip()

    len_text1 = len(text1)
    len_text2 = len(text2)
    # print(len_text1, len_text2)

    try:
        if (len_text1 > 160 and len_text2 > 160):
            text1_lang = detect(text1)
            text2_lang = detect(text2)
        else:
            return jsonify(error_msg="Texten är för kort för att bedömmas (minst 160 tecken)")
    except Exception:
        return jsonify(error_msg = "Skriv in en text")


    try:
        if text1_lang == text2_lang == "en":
            fv_dataframe = IO.create_english_feature_vector(text1, text2)

            df = pd.DataFrame(fv_dataframe)
            abs_fv = abs(df.diff()).dropna()

            x_test = abs_fv.iloc[:,0:len(abs_fv.columns)-1]

            same_user_prob, diff_user_prob = IO.return_eng_result(x_test)

        elif text1_lang == text2_lang == "sv":
            fv_dataframe = IO.create_swedish_feature_vector(text1, text2)

            df = pd.DataFrame(fv_dataframe)
            # print(df)
            abs_fv = abs(df.diff()).dropna()

            x_test = abs_fv.iloc[:,0:len(abs_fv.columns)-1]

            same_user_prob, diff_user_prob = IO.return_swe_result(x_test)

        else:
            return jsonify(error_msg = "Språk ej identifierbart")

        return jsonify(
            same_user_prob = same_user_prob,
            diff_user_prob = diff_user_prob,
            lang = text1_lang
        )

    except Exception:
        traceback.print_exc()
        return jsonify(error_msg = "Ett fel har uppstått")


if __name__ == '__main__':
    app.run(debug=True)
