
    export function find_sum (quantity, value)
    {
        var money = new Array(3).fill(0)
        try {
            var discount = parseInt(this.state.discount_given ? (this.state.discount_given) : 0)
            this.state.items.forEach((item) => {
                let price = parseInt(item.rate)
                let quantity = parseInt(item.quantity)
                money[0] = parseInt(money[0]) + parseInt(price) * parseInt(quantity)
            });
            money[1] = Math.round((discount * money[0]) / 100.0)
            money[2] = money[0] - money[1]
            return money;
        }
        catch (error) {
            alert("error occurred "+error.toString())
            this.setState({loaded:false})


        }
    }


    export function get_pdf (e) {
        this.setState({loaded:true})
        e.preventDefault();
        axios.post(window.API_URL+'/receipts/', this.state)
            .then(response => {
                this.setState({loaded:false})
                if (response.status == 200) {
                        window.open(window.API_URL + response.data.Data.receipt_link);
                }
                else {
                    alert("erro occurred: Unknown error occurred")
                    this.setState({loaded:false})

                }
            })
            .catch(error => {

                alert("error occurred "+error.toString())
                this.setState({loaded:false})

            });
    }