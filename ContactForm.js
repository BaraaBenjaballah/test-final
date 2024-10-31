import React from 'react';
import Swal from 'sweetalert2';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import './ContactForm.css';

// Schéma de validation Yup
const validationSchema = Yup.object().shape({
  nom: Yup.string().required('Le nom est requis'),
  email: Yup.string().email('Email invalide').required('L\'email est requis'),
  cin: Yup.string().required('Le CIN est requis'),
  message: Yup.string().required('Le message est requis'),
});

export default function ContactForm() {
  const handleSubmit = (values, { setSubmitting, resetForm }) => {
    console.log('Données envoyées:', values); 
    axios.post("http://localhost:5000/message", values)
      .then(response => {
        Swal.fire({
          position: 'top',
          icon: 'success',
          title: 'Votre message a été enregistré',
          showConfirmButton: false,
          timer: 1500
        });
        resetForm(); // Réinitialiser le formulaire après soumission
      })
      .catch(error => {
        // Afficher un message d'erreur plus détaillé si possible
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: error.response?.data?.error || 'Quelque chose s\'est mal passé!',
          timer: 1500
        });
      })
      .finally(() => {
        setSubmitting(false);
      });
  };

  return (
    <div className="container">
      <div className="form-container">
        <Formik
          initialValues={{ nom: '', email: '', cin: '', message: '' }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form className="form">
              <div className="form-group">
                <label htmlFor="nom" className="form-label">Nom</label>
                <Field
                  type="text"
                  name="nom"
                  id="nom" // Ajout de l'attribut id
                  placeholder="Nom"
                  className="form-control"
                />
                <ErrorMessage name="nom" component="div" className="error" />
              </div>
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email</label>
                <Field
                  type="email"
                  name="email"
                  id="email" // Ajout de l'attribut id
                  placeholder="Email"
                  className="form-control"
                />
                <ErrorMessage name="email" component="div" className="error" />
              </div>
              <div className="form-group">
                <label htmlFor="cin" className="form-label">Cin</label>
                <Field
                  type="text"
                  name="cin"
                  id="cin" // Ajout de l'attribut id
                  placeholder="Cin"
                  className="form-control"
                />
                <ErrorMessage name="cin" component="div" className="error" />
              </div>
              <div className="form-group">
                <label htmlFor="message" className="form-label">Message</label>
                <Field
                  as="textarea"
                  name="message"
                  id="message" // Ajout de l'attribut id
                  rows="3"
                  placeholder="Envoyer votre message"
                  className="form-control textarea-control"
                />
                <ErrorMessage name="message" component="div" className="error" />
              </div>
              <button
                type="submit"
                className="submit-button"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Envoi...' : 'Envoyer'}
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}
