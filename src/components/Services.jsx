import React, { Component } from "react";
import { Sidebar, Footer, Divider, Content, Header, Container } from 'rsuite';
import { NavbarComponent, NavSideBarComponent } from "./common/NavBar";
import { Datatable } from "./common/Datatable";


class Services extends Component {
    render() {
        const columns = [
            {
                name: 'Id',
                selector: 'id',
                sortable: true,
                maxWidth: "100px"
            },
            {
                name: 'Service Name',
                selector: 'service_name',
                sortable: true,
                maxWidth: "400px"
            },
            {
                name: 'Description',
                selector: 'description',
                sortable: true,
                wrap: true
            }
        ];
        return (
            <Container>
                <Header>
                    <NavbarComponent />
                    <Divider />
                </Header>
                <Container>
                    <Sidebar>
                        <NavSideBarComponent activeKey={"3"} />
                    </Sidebar>
                    <Content>
                        <Datatable title={"Services"} columns={columns} endpoint={"/service"} data={2}/>
                    </Content>
                </Container>
                <Footer></Footer>
            </Container>
        );
    }
}


export default Services;