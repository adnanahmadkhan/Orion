import React, { Component, Fragment } from "react";
import { FormGroup, Col, Button } from "reactstrap";
import jwt_decode from "jwt-decode";

import * as toastr from 'toastr';

import {
    Formik,
    Form,
    Field,
    ErrorMessage,
} from 'formik';
import * as Yup from 'yup';
// import Label from "reactstrap/lib/Label";
import NavbarComponent from "./common/NavBar";
import AuthService from './../services/Auth'
import Auth from "../stores/Auth";

class UserDetails extends Component {
    saveAndContinue = e => {
        e.preventDefault();
        this.props.nextStep();
    };

    render() {
        return (
            <Fragment>
                <NavbarComponent {...this.props} />
                <div className="d-flex align-items-center flex-column  h-100 text-white" >
                    <h3 className="display-4" style={{ marginTop:'50px', padding: '5px', color: 'white', fontSize: '40px',marginRight:'300px' }}>Login </h3>
                    <div className="col-md-4" style={{ paddingTop: '15px', borderRadius: '10px' }} >
                        <Formik
                            initialValues={{
                                username: '',
                                password: '',
                            }}
                            validationSchema={Yup.object().shape({
                                username: Yup.string()
                                    .required('Username is required'),
                                password: Yup.string()
                                    .min(6, 'Password must be at least 6 characters')
                                    .required('Password is required'),
                            })}
                            onSubmit={fields => {

                                let auth = new AuthService();


                                auth.signIn(fields).then(response => {
                                    if (!response.is_error) {
                                        // toastr.success(response.content.message.toString());
                                        const decoded = jwt_decode(response.content.access_token)
                                        Auth.setUser(decoded.identity);

                                        this.props.history.push("/profile",{ response: response.content.message });
                                    }
                                    else{
                                        // debugger
                                        toastr.error(response.error_content.error.toString());
                                    }
                                })
                            }}
                            render={({ errors, status, touched }) => (
                                <Form autocomplete="off">
                                    <FormGroup>
                                        <Col sm="12" md={{ size: 9, offset: 5 }}>
                                        </Col>
                                    </FormGroup>

                                    <FormGroup>
                                        <Col sm="12" md={{ size: 12, offset: 0 }}>
                                            <Field autocomplete="off" auto name="username" placeholder="Username" type="text" className={'form-control-transparent' + (errors.username && touched.username ? ' is-invalid' : '')} />
                                            <ErrorMessage name="username" component="div" className="invalid-feedback" />
                                        </Col>
                                    </FormGroup>

                                    <FormGroup>
                                        <Col sm="12" md={{ size: 12, offset: 0 }}>
                                            <Field autocomplete="off" name="password" type="password" placeholder="Password" className={'form-control-transparent' + (errors.password && touched.password ? ' is-invalid' : '')} />
                                            <ErrorMessage name="password" component="div" className="invalid-feedback" />
                                        </Col>
                                    </FormGroup>

                                    <FormGroup>
                                        <Button type="Submit"  className=" float-right login-button ">
                                            Log In

                                        </Button>

                                    </FormGroup>
                                </Form>
                            )}
                        />
                    </div>
                </div>
            </Fragment>
        );
    }
}

export default UserDetails;
