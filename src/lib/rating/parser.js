class RatingSystem {

    constructor() {
        this.name = "MyRatingSystem"
        this.elements = []
    }

    parse(jsonobj) {
        let name = jsonobj.name;
        delete jsonobj.name;
        if (!jsonobj.elements) {
            throw {
                name: "InvalidDataError",
                message: "Please create elements"
            }
        }
        let parsed_elements = []
        if(Object.keys(jsonobj.elements).length == 0) {
            throw {
                name: "RatingEmptyError",
                message: "Please add some groups or categories to the system"
            }
        
        } else {
            
            if(jsonobj.settings) {
                this.__parse_settings(jsonobj.settings)
            }

            for (const [group_or_cat, value] of Object.entries(jsonobj.elements)) {

                if(typeof value === "object") {
                    if (Object.keys(value).length === 0) {
                        throw {
                            name: "NullGroupError",
                            message: `Please assign data to the group ${group_or_cat}`
                        }
                    }
                    if ("weight" in value) {
                        let name = group_or_cat
                        let group = value
    
                        //parse as group
                        let g;
                        try {
                            g = this.__parse_group(name, group)
    
                        } catch (error) {
                            if(error.name === "ParseAsCategory") {
                                let pweight = parseFloat(value["weight"])
                                if(isNaN(pweight)) {
                                    throw {
                                        name: "InvalidTypeError",
                                        message: `Please assign a valid weight number to the category ${name}`
                                    }
                                } else {
                                    g = new Category(name, pweight)
                                }
                            } else {
                                throw error
                            }
                        }
    
                        parsed_elements.push(g)
                        //console.log(`Parsed elements = ${JSON.stringify(parsed_elements, null, 4)}`)
                    } else if("categories" in value) {
                        throw {
                            name: "NullWeightError",
                            message: `Please assign a weight to the group ${group_or_cat}`
                        }
                    }   
                } else if(typeof value === "number") {
                    let category = group_or_cat
                    parsed_elements.push(new Category(category, value))

                } else {
                    throw {
                        name: "InvalidTypeError",
                        message: `Please assign a valid number to the category ${group_or_cat} or convert it to a group`
                    }
                }
            }
        }
        this.elements = parsed_elements
        console.log(parsed_elements)
    }

    __parse_group(name, group) {

        if("categories" in group && Object.keys(group["categories"]).length > 0) {
            let categories = []

            let group_weight = parseFloat(group["weight"])
            if (isNaN(group_weight)) {
                throw {
                    name: "InvalidWeightError",
                    message: `Please assign a valid number to the weight of the group ${name}`
                }
            }

            //check if every category complies with the schema of "category": weight
            for (const [cat, weight] of Object.entries(group["categories"])) {
                
                let pweight = parseFloat(weight)
                if(isNaN(pweight)) {
                    
                    throw {
                        name: "InvalidWeightError",
                        message: `Please assign a valid number to the weight in ${name} -> ${cat}`
                    }
                } else {
                    categories.push(new Category(cat, pweight))
                }
                
            }
            return new Group(name, group_weight, categories)
        } else {
            console.log(`[WARNING]: Categories not found in group ${name}, the parser will treat it as a single category`)
            
            throw {
                name: "ParseAsCategory"
            }
        }

    }

    __parse_settings(settings) {
        for(const [k, v] of Object.entries(settings)) {
            //TODO: if v in available settings
            if(typeof v === "boolean") {
                this.elements.push(new Setting(k, v))
            }
            
        }
    }

    check_global_weights() {

        let groups = [];
        let categories = [];
        let global_weight = 0;

        for(let el of this.elements) {
            if (el instanceof Group) {
                groups.push(el)
            } else {
                if (el instanceof Setting) {
                    continue
                } else {
                    categories.push(el)
                }
            }
            
        }
        for(let group of groups) {
            global_weight += group.weight
        }
        for(let cat of categories) {
            global_weight += cat.weight
        }

        if(global_weight > 100) {
            throw {
                name: "GlobalWeightError",
                message: `The global weight is ${global_weight}.The weight (%) of all the rating system can't be bigger than 100%!`
            }
        } else if (global_weight < 100) {
            throw {
                name: "GlobalWeightError",
                message: `The global weight is ${global_weight}. The weight (%) of all the rating system can't be less than 100%!`
            }
        } else {
            return groups
        }
        //now check local weights
        
    }

    check_local_weights(groups) {

        for(let group of groups) {
            let local_weight = 0;
            for(let cat of group.categories) {
                local_weight += cat.weight
            }
            if(local_weight > 100) {
                throw {
                    name: "LocalWeightError",
                    message: `The local weight is ${local_weight}.The weight (%) of the categories in group ${group.name} can't be bigger than 100%!`,
                    value: group.name
                }
            } else if (local_weight < 100) {
                throw {
                    name: "GlobalWeightError",
                    message: `The local weight is ${local_weight}. The weight (%) of the categories in group ${group.name} can't be less than 100%!`,
                    value: group.name
                }
            } else {
                console.log(`INFO: Local weight of group ${group.name} is correct.`)
            }
        }
    }
}

class Group {
    constructor(name, weight, categories) {
        this.name = name
        this.weight = weight,
        this.categories = categories
    }
}


class Category {
    constructor(name, weight) {
        this.name = name,
        this.weight = weight
    }
}

class Setting {
    constructor(name, value) {
        this.name = name,
        this.value = value
    }
}

let example = {
    "name": "MyRatingSystem",
    "elements": {
        "Art": {
            "weight": 40,
            "categories": {
                "graphics": 40,
                "animations": 40,
                "other": 20
            }
        },
        "Bruh": {
            "weight": 20,
            "categories": {
                "graphics": 40,
                "animations": 40,
                "other": 20
            },
        },
        "Music": {
            "weight": 20,
            
        },
        "Test": 20,
        "__enable_extras": true
    }
}
// let rs = new RatingSystem(example["name"])
// //why does the parser automatically delete duplicate groups (name)?
// rs.parse(example["elements"])
// console.log(rs.elements)
// rs.check_weights()
export {RatingSystem, Category, Group, Setting}