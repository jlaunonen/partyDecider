/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface Ballot
 */
export interface Ballot {
    /**
     * 
     * @type {{ [key: string]: number; }}
     * @memberof Ballot
     */
    ballot: { [key: string]: number; };
}

/**
 * Check if a given object implements the Ballot interface.
 */
export function instanceOfBallot(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "ballot" in value;

    return isInstance;
}

export function BallotFromJSON(json: any): Ballot {
    return BallotFromJSONTyped(json, false);
}

export function BallotFromJSONTyped(json: any, ignoreDiscriminator: boolean): Ballot {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'ballot': json['ballot'],
    };
}

export function BallotToJSON(value?: Ballot | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'ballot': value.ballot,
    };
}

