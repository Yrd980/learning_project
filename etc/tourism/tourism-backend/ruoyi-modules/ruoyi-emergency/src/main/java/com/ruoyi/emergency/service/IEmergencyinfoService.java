package com.ruoyi.emergency.service;

import java.util.List;
import com.ruoyi.emergency.domain.Emergencyinfo;

/**
 * 应急信息Service接口
 * 
 * @author ningf
 * @date 2024-07-12
 */
public interface IEmergencyinfoService 
{
    /**
     * 查询应急信息
     * 
     * @param id 应急信息主键
     * @return 应急信息
     */
    public Emergencyinfo selectEmergencyinfoById(Long id);

    /**
     * 查询应急信息列表
     * 
     * @param emergencyinfo 应急信息
     * @return 应急信息集合
     */
    public List<Emergencyinfo> selectEmergencyinfoList(Emergencyinfo emergencyinfo);

    /**
     * 新增应急信息
     * 
     * @param emergencyinfo 应急信息
     * @return 结果
     */
    public int insertEmergencyinfo(Emergencyinfo emergencyinfo);

    /**
     * 修改应急信息
     * 
     * @param emergencyinfo 应急信息
     * @return 结果
     */
    public int updateEmergencyinfo(Emergencyinfo emergencyinfo);

    /**
     * 批量删除应急信息
     * 
     * @param ids 需要删除的应急信息主键集合
     * @return 结果
     */
    public int deleteEmergencyinfoByIds(Long[] ids);

    /**
     * 删除应急信息信息
     * 
     * @param id 应急信息主键
     * @return 结果
     */
    public int deleteEmergencyinfoById(Long id);

    public int confirmEmergencyinfoByIds(Long[] ids);
}
