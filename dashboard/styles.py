def load_css():

    return """
    <style>

    /* ---------------------------------------------------- */
    /* Main App */
    /* ---------------------------------------------------- */

    .main{

        padding-top:1rem;

        padding-left:2rem;

        padding-right:2rem;

    }

    /* ---------------------------------------------------- */
    /* Hero Title */
    /* ---------------------------------------------------- */

    .main-title{

        font-size:42px;

        font-weight:800;

        color:#2563EB;

        margin-bottom:0px;

    }

    .sub-title{

        font-size:18px;

        color:#6B7280;

        margin-bottom:25px;

    }

    /* ---------------------------------------------------- */
    /* Metric Cards */
    /* ---------------------------------------------------- */

    div[data-testid="metric-container"]{

        background-color:#FFFFFF;

        border:1px solid #E5E7EB;

        padding:18px;

        border-radius:14px;

        box-shadow:0px 2px 10px rgba(0,0,0,0.05);

    }

    /* ---------------------------------------------------- */
    /* Buttons */
    /* ---------------------------------------------------- */

    .stButton>button{

        width:100%;

        border-radius:10px;

        height:48px;

        font-size:18px;

        font-weight:600;

    }

    /* ---------------------------------------------------- */
    /* Text Area */
    /* ---------------------------------------------------- */

    textarea{

        border-radius:12px !important;

    }

    /* ---------------------------------------------------- */
    /* Dataframe */
    /* ---------------------------------------------------- */

    .stDataFrame{

        border-radius:12px;

        overflow:hidden;

    }

    /* ---------------------------------------------------- */
    /* Tabs */
    /* ---------------------------------------------------- */

    button[data-baseweb="tab"]{

        font-size:16px;

        font-weight:600;

    }

    /* ---------------------------------------------------- */
    /* Success Messages */
    /* ---------------------------------------------------- */

    div[data-testid="stAlert"]{

        border-radius:12px;

    }

    /* ---------------------------------------------------- */
    /* Horizontal Rule */
    /* ---------------------------------------------------- */

    hr{

        margin-top:30px;

        margin-bottom:30px;

    }

    </style>
    """