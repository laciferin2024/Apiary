use alloy::primitives::FixedBytes;
use pyo3::exceptions::PyValueError;

use pyo3::prelude::*;
use crate::apiary::erc_for_job;

#[tokio::main]
#[pyfunction]
async fn helloworld() -> PyResult<String> {
    Ok("HelloWorld ERC".into())
}

#[pyclass]
pub enum BuyStatement {
    ERC20(String, u64, String, String),
    ERC721(String, u64, String, String),
    Bundle(Vec<String>, Vec<u64>, Vec<String>, Vec<u64>, String, String),
}

#[tokio::main]
#[pyfunction]
async fn get_buy_statement(
    statement_uid: String,
) -> PyResult<BuyStatement> {
    let statement_uid: FixedBytes<32> = statement_uid
        .parse::<FixedBytes<32>>()
        .map_err(|_| PyValueError::new_err("couldn't parse statement_uid as bytes32"))?;

    let payment_result = erc_for_job::get_buy_statement(statement_uid)
        .await
        .map_err(PyErr::from)?;

    match payment_result.price {
        erc_for_job::JobPrice::ERC20(price) => {
            let result = BuyStatement::ERC20(
                price.token.to_string(),
                price.amount.try_into()
                    .map_err(|_| PyValueError::new_err("amount too big for u64"))?,
                payment_result.arbiter.to_string(),
                payment_result.demand.result.to_string(),
            );
            Ok(result)
        },
        erc_for_job::JobPrice::ERC721(price) => {
            let result = BuyStatement::ERC721(
                price.token.to_string(),
                price.id.try_into()
                    .map_err(|_| PyValueError::new_err("amount too big for u64"))?,
                payment_result.arbiter.to_string(),
                payment_result.demand.result.to_string(),
            );
            Ok(result)
        },
        erc_for_job::JobPrice::Bundle(price) => {
            let result = BuyStatement::Bundle(
                price.erc20_addresses.iter()
                .map(|address| address.to_string())
                .collect::<Vec<String>>(),

                price.erc20_amounts
                .iter()
                .map(|amount| {
                    <&alloy::primitives::Uint<256, 4> as TryInto<u64>>::try_into(amount)
                    .map_err(|_| PyValueError::new_err("amount too big for u64"))
                })
                .collect::<Result<Vec<u64>, _>>()?,

                price.erc721_addresses
                .iter()
                .map(|address| address.to_string())
                .collect::<Vec<String>>(),

                price.erc721_ids
                    .iter()
                    .map(|amount| {
                        <&alloy::primitives::Uint<256, 4> as TryInto<u64>>::try_into(amount)
                        .map_err(|_| PyValueError::new_err("amount too big for u64"))
                })
                .collect::<Result<Vec<u64>, _>>()?,

                payment_result.arbiter.to_string(),
                payment_result.demand.result.to_string(),
            );
            Ok(result)
        },
    }
}

#[tokio::main]
#[pyfunction]
pub async fn get_sell_statement(
    sell_uid: String,
) -> PyResult<String> {

    let sell_uid = sell_uid
    .parse::<FixedBytes<32>>()
    .map_err(|_| PyValueError::new_err("couldn't parse sell_uid as bytes32"))?;

    let result_cid = erc_for_job::get_sell_statement(sell_uid)
    .await
    .map_err(PyErr::from)?;

    Ok(result_cid)
}

pub fn add_erc_submodule(py: Python, parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let erc_module = PyModule::new_bound(py, "erc")?;

    erc_module.add_function(wrap_pyfunction!(helloworld, &erc_module)?)?;

    erc_module.add_class::<BuyStatement>()?;
    erc_module.add_function(wrap_pyfunction!(get_buy_statement, &erc_module)?)?;
    erc_module.add_function(wrap_pyfunction!(get_sell_statement, &erc_module)?)?;

    parent_module.add_submodule(&erc_module)?;
    Ok(())
}
