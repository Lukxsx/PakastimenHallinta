import datetime

from flask import redirect, render_template, url_for
from flask_login import login_required, current_user

from application import app, db
from application.elintarvike.models import Elintarvike
from application.elintarvikekaapissa.models import ElintarvikeKaapissa
from application.kaappi.models import Kaappi


class Vanhentunut:
    def __init__(self, ek, pvm, paivia):
        self.ek = ek
        self.pvm = pvm
        self.paivia = paivia

    def tulostaVanhentunutPvm(self):
        return "" + str(self.pvm.day) + "." + str(self.pvm.month) + "." + str(self.pvm.year)


@app.route("/paivays", methods=["GET"])
@login_required
def vanhentuneet():
    today = datetime.date.today()
    ek = ElintarvikeKaapissa.query.filter_by(kayttaja_id=current_user.id).all()
    vanhentuneet = []
    for elink in ek:
        s = Elintarvike.query.filter_by(id=elink.elintarvike_id).first()
        laitettu = elink.laitettu_kaappiin
        vanhenee = laitettu + datetime.timedelta(days=s.sailyvyys)
        if vanhenee < today:
            paivia = (today - vanhenee).days
            vanhentunut = Vanhentunut(elink, vanhenee, paivia)
            vanhentuneet.append(vanhentunut)

    return render_template("paivays/listaa.html", lista=vanhentuneet, elin=Elintarvike, kaappi=Kaappi)


@app.route("/paivays/poista/<ek_id>/", methods=["POST"])
@login_required
def vanhentuneen_poistaja(ek_id):
    poistettava = ElintarvikeKaapissa.query.get(ek_id)
    db.session.delete(poistettava)
    db.session.commit()

    return redirect(url_for("vanhentuneet"))
