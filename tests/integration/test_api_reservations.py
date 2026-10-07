CRENEAU_DEMAIN = {"debut": "2026-10-08T10:00:00", "fin": "2026-10-08T12:00:00"}


def test_reserver_creneau_libre_puis_conflit(client_http):
    premiere = client_http.post(
        "/reservations", json={"client_id": 1, "vehicule_id": 1, **CRENEAU_DEMAIN}
    )
    assert premiere.status_code == 201
    assert premiere.json()["statut"] == "CONFIRMEE"

    seconde = client_http.post(
        "/reservations", json={"client_id": 2, "vehicule_id": 1, **CRENEAU_DEMAIN}
    )
    assert seconde.status_code == 409
    assert seconde.json()["erreur"] == "CONFLIT_RESERVATION"


def test_scenario_nominal_reserver_puis_consulter(client_http):
    reponse = client_http.post(
        "/reservations",
        json={"client_id": 1, "vehicule_id": 2, "debut": "2026-10-08T10:00:00", "fin": "2026-10-08T11:30:00"},
    )
    assert reponse.status_code == 201
    reservation = reponse.json()
    assert reservation == {
        "id": 1,
        "client_id": 1,
        "vehicule_id": 2,
        "debut": "2026-10-08T10:00:00",
        "fin": "2026-10-08T11:30:00",
        "statut": "CONFIRMEE",
        "montant_estime_centimes": 600,
    }

    consultee = client_http.get(f"/reservations/{reservation['id']}")
    assert consultee.status_code == 200
    assert consultee.json() == reservation


def test_consulter_reservation_inconnue(client_http):
    reponse = client_http.get("/reservations/999")
    assert reponse.status_code == 404
    assert reponse.json()["erreur"] == "RESERVATION_INTROUVABLE"


def test_vehicule_en_maintenance(client_http):
    reponse = client_http.post("/reservations", json={"client_id": 1, "vehicule_id": 3, **CRENEAU_DEMAIN})
    assert reponse.status_code == 409
    assert reponse.json()["erreur"] == "VEHICULE_INDISPONIBLE"


def test_creneau_dans_le_passe(client_http):
    reponse = client_http.post(
        "/reservations",
        json={"client_id": 1, "vehicule_id": 1, "debut": "2026-10-06T10:00:00", "fin": "2026-10-06T11:00:00"},
    )
    assert reponse.status_code == 422
    assert reponse.json()["erreur"] == "CRENEAU_DANS_LE_PASSE"


def test_date_avec_fuseau_convertie_en_utc_et_conflit_detecte(client_http):
    reponse = client_http.post(
        "/reservations",
        json={"client_id": 1, "vehicule_id": 1, "debut": "2026-10-08T10:00:00+02:00", "fin": "2026-10-08T12:00:00+02:00"},
    )
    assert reponse.status_code == 201
    assert reponse.json()["debut"] == "2026-10-08T08:00:00"

    conflit = client_http.post(
        "/reservations",
        json={"client_id": 2, "vehicule_id": 1, "debut": "2026-10-08T09:00:00Z", "fin": "2026-10-08T09:30:00Z"},
    )
    assert conflit.status_code == 409
    assert conflit.json()["erreur"] == "CONFLIT_RESERVATION"
