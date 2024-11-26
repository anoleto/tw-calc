use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn calculate_tw_multiplier(tw: f64) -> f64 {
    // https://github.com/refx-online/refx-pp-rs/blob/16a0466cf164ea628ae9271b1f18a51d765f9781/src/osu_2019/pp.rs#L474

    // punish for tw less than 100:
    // - calculate a penalty based on how far tw is below 100.
    // - we use a quadratic scaling factor: (4.0 * (100.0 - tw) / 100.0)^2.
    // - then cap the result at a maximum of -0.048 to avoid excessive penalties.
    // - multiply by the condition (tw < 100.0) as a boolean (cast to u8, then to f64).\
    // - tbh i should rework this.. 90-95 is -0.048. thats bad
    -((4.0 * (100.0 - tw) / 100.0)
        .powi(2))
        .min(0.048) * 
    (tw < 100.0) as u8 as f64

    // award for tw more than 100:
    // - calculate a scaling factor based on how far tw is above 100.
    // - use an exponential scaling factor: (1.02)^((tw - 100.0) / 5.0 - 1.0).
    // - we adjust the result by dividing by 150.0.
    // - then multiply by the condition (tw > 103.0) as a boolean (cast to u8, then to f64).
    // - why we checks for tw > 103.0 instead of 100.0? because 101.0 gives around 0.006666666666666667 multiplier, we dont want that
    + ((tw - 100.0) * (1.02_f64)
        .powf((tw - 100.0)
        .max(0.0) / 5.0 - 1.0) / 150.0) * 
    (tw > 103.0) as u8 as f64

    // why is as "u8" instead of if checks?
    // look funny :p should be look more cancerous tho
}

#[pymodule]
fn thecalc(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_tw_multiplier, m)?)?;
    Ok(())
}