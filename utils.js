function zip(arr1, arr2) {
    const c = arr1.map((val, index) => ([val, arr2[index]]));
    return c;
}

module.exports = {
    zip
};
